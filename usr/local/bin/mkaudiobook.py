#!/usr/bin/env python3
"""
mkaudio - Build per-chapter audio from Markdown chapter sources.

Reads the same {lang}/NNNN - Title.md layout as mkbook, strips Markdown
to prose suitable for text-to-speech, and synthesizes one M4A file per
chapter. Cleaned prose is written alongside as .txt.

Output layout:
    {lang}/audio/m4a/NNNN - Title.m4a
    {lang}/audio/text/NNNN - Title.txt

Config: book.json (same file mkbook reads, under the "audio" key).

Backends: say (macOS), piper (offline neural), espeak-ng (Linux).
Requires: ffmpeg on PATH for transcoding.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_AUDIO = {
    "engine": "say",
    "voice": {},
    "rate": 175,
    "bitrate": "64k",
    "sample_rate": 22050,
}


def load_config(path="book.json"):
    if not Path(path).exists():
        sys.exit(f"Error: Configuration file '{path}' not found.")
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    for key in ("source_lang", "languages"):
        if key not in config:
            sys.exit(f"Missing required config key: '{key}'")
    audio = dict(DEFAULT_AUDIO)
    audio.update(config.get("audio", {}))
    config["audio"] = audio
    return config


# ---------------------------------------------------------------------------
# Markdown → prose
# ---------------------------------------------------------------------------

_FRONTMATTER = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
_FENCED_CODE = re.compile(r"^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$", re.MULTILINE | re.DOTALL)
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_HTML_TAG = re.compile(r"</?[a-zA-Z][^>]*>")
_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)|!\[[^\]]*\]\[[^\]]*\]")
_LINK_DEF = re.compile(r"^\s*\[[^\]]+\]:\s*\S+.*$", re.MULTILINE)
_LINK_INLINE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_LINK_REF = re.compile(r"\[([^\]]+)\]\[[^\]]*\]")
_FOOTNOTE_REF = re.compile(r"\[\^[^\]]+\]")
_FOOTNOTE_DEF = re.compile(r"^\s*\[\^[^\]]+\]:\s*.*$", re.MULTILINE)
_SETEXT_H1 = re.compile(r"^(?P<text>[^\n]+)\n=+\s*$", re.MULTILINE)
_SETEXT_H2 = re.compile(r"^(?P<text>[^\n]+)\n-+\s*$", re.MULTILINE)
_HR = re.compile(r"^\s*([-*_])(?:\s*\1){2,}\s*$", re.MULTILINE)
_ATX_H = re.compile(r"^\s*#{1,6}\s+(.*?)\s*#*\s*$", re.MULTILINE)
_BLOCKQUOTE = re.compile(r"^\s*>\s?", re.MULTILINE)
_UL = re.compile(r"^\s*[-*+]\s+", re.MULTILINE)
_OL = re.compile(r"^\s*\d+[.)]\s+", re.MULTILINE)


def strip_markdown(text: str) -> str:
    # 1. YAML frontmatter at the top of the file.
    text = _FRONTMATTER.sub("", text, count=1)

    # 2. Fenced code blocks. Reading code aloud is noise, so drop entirely.
    text = _FENCED_CODE.sub("", text)

    # 3. HTML comments first (they can contain ">" characters that would
    #    confuse the tag stripper), then tags.
    text = _HTML_COMMENT.sub("", text)
    text = _HTML_TAG.sub("", text)

    # 4. Images. Alt text is almost never meant to be read; drop entirely.
    #    Must come before links, since ![alt](url) contains [alt](url).
    text = _IMAGE.sub("", text)

    # 5. Footnotes: drop both the inline markers and the definition lines.
    text = _FOOTNOTE_REF.sub("", text)
    text = _FOOTNOTE_DEF.sub("", text)

    # 6. Reference-style link definitions ("[1]: http://…").
    text = _LINK_DEF.sub("", text)

    # 7. Inline and reference links → keep the link text only.
    text = _LINK_INLINE.sub(r"\1", text)
    text = _LINK_REF.sub(r"\1", text)

    # 8. Setext headings must run before HR: both use --- / === underlines
    #    and only the surrounding context distinguishes them.
    text = _SETEXT_H1.sub(lambda m: m.group("text").strip() + ".", text)
    text = _SETEXT_H2.sub(lambda m: m.group("text").strip() + ".", text)

    # 9. Horizontal rules — anything left that is only rule characters.
    text = _HR.sub("", text)

    # 10. ATX headings. Keep the text, add a period so the TTS engine
    #     produces a natural pause after the chapter title.
    text = _ATX_H.sub(lambda m: m.group(1).rstrip(".") + ".", text)

    # 11. Blockquote and list markers.
    text = _BLOCKQUOTE.sub("", text)
    text = _UL.sub("", text)
    text = _OL.sub("", text)

    # 12. Emphasis. Longest markers first, otherwise *** is eaten by **.
    text = re.sub(r"\*\*\*([^*]+)\*\*\*", r"\1", text)
    text = re.sub(r"___([^_]+)___", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"\*([^*\n]+)\*", r"\1", text)
    # Only strip _emphasis_ when it isn't inside a word (e.g. snake_case).
    text = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"\1", text)

    # 13. Inline code and strikethrough.
    text = re.sub(r"`([^`\n]+)`", r"\1", text)
    text = re.sub(r"~~([^~]+)~~", r"\1", text)

    # 14. Typographic cleanup. Curly quotes are fine on macOS say but some
    #     engines (espeak) choke, and dashes get read as "dash" otherwise.
    text = text.replace("\u00a0", " ")
    text = text.replace("\u2014", ", ").replace("\u2013", ", ")
    text = text.replace("\u2026", "...")
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2022", ", ")

    # 15. Collapse whitespace and orphan punctuation from steps 12–14.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"\.\s*,", ".", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)

    return text.strip()


# ---------------------------------------------------------------------------
# TTS backends
# ---------------------------------------------------------------------------

class SayBackend:
    """macOS built-in `say`."""

    def __init__(self, cfg):
        self.voices = cfg.get("voice") or {}
        self.rate = cfg.get("rate")

    def _voice(self, lang):
        if isinstance(self.voices, str):
            return self.voices
        return self.voices.get(lang)

    def synthesize(self, text: str, out_stem: Path, lang: str) -> Path:
        out = out_stem.with_suffix(".aiff")
        cmd = ["say", "-o", str(out)]
        if self.rate:
            cmd += ["-r", str(self.rate)]
        v = self._voice(lang)
        if v:
            cmd += ["-v", v]
        subprocess.run(cmd, input=text.encode("utf-8"), check=True)
        return out


class PiperBackend:
    """Offline neural TTS. Needs `piper` on PATH and one ONNX model per language."""

    def __init__(self, cfg):
        self.bin = cfg.get("piper_bin", "piper")
        self.models = cfg.get("piper_models") or {}

    def synthesize(self, text: str, out_stem: Path, lang: str) -> Path:
        model = self.models.get(lang) or self.models.get("default")
        if not model:
            sys.exit(f"piper: no model configured for language '{lang}'")
        out = out_stem.with_suffix(".wav")
        cmd = [self.bin, "-m", model, "-f", str(out)]
        subprocess.run(cmd, input=text.encode("utf-8"), check=True)
        return out


class EspeakBackend:
    """espeak-ng — the pragmatic Linux fallback."""

    def __init__(self, cfg):
        self.voices = cfg.get("voice") or {}
        self.rate = cfg.get("rate")

    def synthesize(self, text: str, out_stem: Path, lang: str) -> Path:
        out = out_stem.with_suffix(".wav")
        voice = self.voices.get(lang) if isinstance(self.voices, dict) else self.voices
        cmd = ["espeak-ng", "-w", str(out)]
        if voice:
            cmd += ["-v", voice]
        if self.rate:
            cmd += ["-s", str(self.rate)]
        subprocess.run(cmd, input=text.encode("utf-8"), check=True)
        return out


def make_backend(cfg):
    name = cfg.get("engine", "say")
    if name == "say":
        if sys.platform != "darwin":
            sys.exit("The 'say' engine is macOS-only; configure another in book.json.")
        if not shutil.which("say"):
            sys.exit("'say' not found on PATH.")
        return SayBackend(cfg)
    if name == "piper":
        if not shutil.which(cfg.get("piper_bin", "piper")):
            sys.exit("'piper' not found on PATH.")
        return PiperBackend(cfg)
    if name == "espeak":
        if not shutil.which("espeak-ng"):
            sys.exit("'espeak-ng' not found on PATH.")
        return EspeakBackend(cfg)
    sys.exit(f"Unknown audio engine: {name!r}")


# ---------------------------------------------------------------------------
# Transcoding
# ---------------------------------------------------------------------------

def transcode_to_m4a(src: Path, dst: Path, cfg):
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(src),
        "-c:a", "aac", "-b:a", cfg["bitrate"],
        "-ar", str(cfg["sample_rate"]), "-ac", "1",
        str(dst),
    ], check=True)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def process_language(lang_dir, config, args):
    cfg = config["audio"]
    lang_path = Path(lang_dir)
    md_files = sorted(lang_path.glob("*.md"))
    if not md_files:
        print(f"  No .md files in {lang_dir}, skipping.")
        return

    audio_dir = lang_path / "audio"
    m4a_dir = audio_dir / "m4a"
    text_dir = audio_dir / "text"
    m4a_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)

    backend = None if args.text_only else make_backend(cfg)

    for md in md_files:
        prose = strip_markdown(md.read_text(encoding="utf-8"))
        if not prose:
            continue

        # Always write cleaned prose.
        (text_dir / f"{md.stem}.txt").write_text(prose, encoding="utf-8")

        if args.text_only:
            print(f"  Text: {md.name}")
            continue

        m4a = m4a_dir / f"{md.stem}.m4a"
        if args.force or not m4a.exists():
            print(f"  Synthesizing: {md.name}")
            raw = backend.synthesize(prose, m4a_dir / md.stem, lang=lang_dir)
            transcode_to_m4a(raw, m4a, cfg)
            raw.unlink(missing_ok=True)
        else:
            print(f"  Cached: {md.name}")


def main():
    ap = argparse.ArgumentParser(description="Build per-chapter audiobooks from Markdown sources.")
    ap.add_argument("-c", "--config", default="book.json")
    ap.add_argument("-l", "--lang", help="Build only the given language folder")
    ap.add_argument("-f", "--force", action="store_true",
                    help="Re-synthesize even if cached chapter audio exists")
    ap.add_argument("--text-only", action="store_true",
                    help="Only write cleaned prose; do not synthesize")
    args = ap.parse_args()

    config = load_config(args.config)

    lang_dirs = sorted(
        d.name for d in Path(".").iterdir()
        if d.is_dir() and d.name in config["languages"]
    )
    if not lang_dirs:
        sys.exit("No language directories found (check 'languages' map).")
    if args.lang:
        if args.lang not in lang_dirs:
            sys.exit(f"Language '{args.lang}' not found among {lang_dirs}")
        lang_dirs = [args.lang]

    if not args.text_only:
        if not shutil.which("ffmpeg"):
            sys.exit("'ffmpeg' is required but not on PATH.")

    for lang in lang_dirs:
        print(f"\n===== Processing language: {lang} =====")
        process_language(lang, config, args)

    print("\nDone.")


if __name__ == "__main__":
    main()