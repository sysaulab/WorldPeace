#!/usr/bin/env python3
"""
mkbook - Build ebooks, PDFs, and plain text from Markdown sources.
Configuration: book.json in the current directory.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def load_config(path="book.json"):
    """Load and validate the JSON configuration."""
    if not os.path.exists(path):
        sys.exit(f"Error: Configuration file '{path}' not found.")
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Basic sanity checks
    required_top = ["source_lang", "languages", "pdf"]
    for key in required_top:
        if key not in config:
            sys.exit(f"Missing required config key: '{key}'")
    if "outputs" not in config["pdf"]:
        sys.exit("No PDF outputs defined (pdf.outputs).")
    return config

def get_metadata_file(lang_dir):
    """Return the metadata.yaml path for a language, or None if absent."""
    meta = Path(lang_dir) / "metadata.yaml"
    return str(meta) if meta.is_file() else None

def run_translation(config, target_lang):
    """Run external translation command if configured."""
    src = config["source_lang"]
    tgt = target_lang
    if src == tgt:
        return  # no self-translation

    # Look up full language names
    src_full = config["languages"].get(src)
    tgt_full = config["languages"].get(tgt)
    if not src_full or not tgt_full:
        sys.exit(f"Missing language mapping for '{src}' or '{tgt}' in 'languages' dict.")

    cmd = [
        config.get("translate_cmd", "translate"),
        "--input-dir", src,
        "--source-lang", src_full,
        "--output-dir", tgt,
        "--target-lang", tgt_full,
        "--no-recursive",
    ]
    print(f"  Translating {src} -> {tgt}: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def build_pdf(md_files, outfile, fmt, config, lang_dir):
    """Build a single PDF using Pandoc."""
    pdf = config["pdf"]
    cmd = ["pandoc", "-s", "-o", outfile]

    meta = get_metadata_file(lang_dir)
    if meta:
        cmd += ["--metadata-file", meta]

    cmd += md_files + [
        "--pdf-engine", pdf["engine"],
        "-V", f"documentclass={pdf['documentclass']}",
        "-V", f"classoption={pdf['classoption']}",
        "-V", f"header-includes={pdf['header_includes']}",
        "-V", f"mainfont={pdf.get('mainfont', 'Times New Roman')}",
    ]
    if "mainfontoptions" in pdf:
        cmd += ["-V", f"mainfontoptions={pdf['mainfontoptions']}"]
    if pdf.get("toc"):
        cmd += ["--toc", "--toc-depth", str(pdf.get("toc_depth", 2))]

    geometry = (
        f"paperwidth={fmt['width']}, paperheight={fmt['height']}, "
        f"inner={fmt['inner']}, outer={fmt['outer']}, "
        f"top={fmt['top']}, bottom={fmt['bottom']}, "
        f"bindingoffset={fmt.get('bindingoffset', '0in')}"
    )
    cmd += ["-V", f"geometry:{geometry}", "-V", f"fontsize={fmt.get('fontsize', '11pt')}"]

    print(f"    Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def impose_pdf(pdf_file, paper):
    """Impose a PDF using pdfbook2."""
    cmd = ["pdfbook2", "-snp", paper, "-o", "0", "-i", "0", "-t", "0", "-b", "0", pdf_file]
    print(f"    Imposing: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def process_language(lang_dir, config, skip_translate=False):
    print(f"\n===== Processing language: {lang_dir} =====")

    if lang_dir != config["source_lang"] and not skip_translate:
        run_translation(config, lang_dir)

    md_files = sorted(Path(lang_dir).glob("*.md"))
    if not md_files:
        print(f"  No .md files found in {lang_dir}, skipping.")
        return
    md_paths = [str(p) for p in md_files]

    meta = get_metadata_file(lang_dir)
    meta_args = ["--metadata-file", meta] if meta else []

    # EPUB
    epub_out = f"{lang_dir}.epub"
    epub_cmd = ["pandoc", "-o", epub_out] + meta_args + md_paths
    cover_img = Path(lang_dir) / config.get("epub", {}).get("cover_image", "cover.jpg")
    if cover_img.is_file():
        epub_cmd += ["--epub-cover-image", str(cover_img)]
    print(f"  Creating {epub_out}")
    subprocess.run(epub_cmd, check=True)

    # Plain text
    txt_out = f"{lang_dir}.txt"
    txt_cmd = ["pandoc", "-o", txt_out] + meta_args + md_paths
    print(f"  Creating {txt_out}")
    subprocess.run(txt_cmd, check=True)

    # PDFs
    for fmt in config["pdf"]["outputs"]:
        outfile = f"{lang_dir}.{fmt['name']}.pdf"
        print(f"  Creating {outfile}")
        build_pdf(md_paths, outfile, fmt, config, lang_dir)
        impose_paper = fmt.get("impose_paper")
        if impose_paper:
            impose_pdf(outfile, impose_paper)

def main():
    parser = argparse.ArgumentParser(description="Build books from Markdown sources.")
    parser.add_argument("-c", "--config", default="book.json", help="Path to config file (default: book.json)")
    parser.add_argument("-l", "--lang", help="Build only the given language folder")
    parser.add_argument("--no-translate", action="store_true", help="Skip translation step")
    args = parser.parse_args()

    config = load_config(args.config)

    # Determine which language directories to process
    all_dirs = [d.name for d in Path(".").iterdir() if d.is_dir()]
    lang_dirs = [d for d in all_dirs if d in config["languages"]]
    if not lang_dirs:
        sys.exit("No language directories found (check 'languages' map).")

    if args.lang:
        if args.lang not in lang_dirs:
            sys.exit(f"Language '{args.lang}' not found among {lang_dirs}")
        lang_dirs = [args.lang]

    for lang in sorted(lang_dirs):
        process_language(lang, config, skip_translate=args.no_translate)

    print("\nAll builds complete.")


if __name__ == "__main__":
    main()
