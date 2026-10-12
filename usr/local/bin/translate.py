#!/usr/bin/env python3
"""
Batch document translation using the DeepSeek API (or local Ollama).
Reads files from --input-dir, translates them to --target-lang,
and writes them to --output-dir, preserving the directory structure.

Modes:
- Default: files are translated in parallel, each file gets its own chat session
  (chunks within a file are serial).
- --serialize-all: all files are translated in one single chat session (serial)
  for maximum book-level consistency. A sliding window keeps only the last N
  user-assistant pairs to stay within context limits.

Uses tiktoken for accurate tokenisation.
"""

import argparse
import logging
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple, Optional
from deepseek_tokenizer import ds_token

import openai

# ----------------------------------------------------------------------
# Dependencies for tokentizing
# ----------------------------------------------------------------------
def count_tokens(text: str) -> int:
    return len(ds_token.encode(text))

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
LOCAL_BASE_URL = "http://localhost:11434/v1"  # Ollama default
DEFAULT_MODEL = "deepseek-chat"
LOCAL_MODEL = "gemma4:e4b"

# ----------------------------------------------------------------------
# Paragraph‑aware chunking (unchanged from previous version)
# ----------------------------------------------------------------------
def split_into_chunks(text: str, max_tokens: int) -> List[Tuple[str, bool]]:
    """
    Returns list of (chunk_text, is_continuation).
    is_continuation=True when the chunk continues the last paragraph
    of the preceding chunk.
    """
    paragraphs = text.split("\n\n")
    chunks_meta: List[Tuple[str, bool]] = []
    current_buf: List[str] = []
    current_tokens = 0

    for para in paragraphs:
        para_tokens = count_tokens(para)

        # Paragraph fits in current chunk
        if current_tokens + para_tokens <= max_tokens:
            current_buf.append(para)
            current_tokens += para_tokens
            continue

        # Flush current chunk if not empty
        if current_buf:
            chunks_meta.append(("\n\n".join(current_buf), False))
            current_buf = []
            current_tokens = 0

        # Paragraph itself fits in one chunk
        if para_tokens <= max_tokens:
            current_buf = [para]
            current_tokens = para_tokens
            continue

        # ----- Paragraph too long → split by sentences -----
        if sent_tokenize:
            sentences = sent_tokenize(para)
        else:
            sentences = [
                s.strip()
                for s in re.split(r"(?<=[.!?])\s+", para)
                if s.strip()
            ]

        sub_buf = []
        sub_tokens = 0
        for sent in sentences:
            sent_tokens = count_tokens(sent)
            if sub_tokens + sent_tokens > max_tokens and sub_buf:
                chunks_meta.append((" ".join(sub_buf), False))
                sub_buf = [sent]
                sub_tokens = sent_tokens
            else:
                sub_buf.append(sent)
                sub_tokens += sent_tokens

        if sub_buf:
            chunks_meta.append((" ".join(sub_buf), True))  # continuation

    # Last chunk
    if current_buf:
        chunks_meta.append(("\n\n".join(current_buf), False))

    return chunks_meta


def reassemble_parts(parts: List[str], flags: List[bool]) -> str:
    """Join translated parts using the continuation flags."""
    result = ""
    for idx, (part, cont) in enumerate(zip(parts, flags)):
        if idx == 0:
            result = part
        elif cont:
            result += " " + part
        else:
            result += "\n\n" + part
    return result


# ----------------------------------------------------------------------
# ChatSession – handles a single chat with a sliding window
# ----------------------------------------------------------------------
class ChatSession:
    """
    Maintains a serial chat for translating multiple documents.
    The sliding window keeps the system message + the last N user‑assistant pairs.
    """

    def __init__(
        self,
        client: openai.OpenAI,
        model: str,
        system_msg: str,
        sliding_window_pairs: int = 16,
    ):
        self.client = client
        self.model = model
        self.messages = [{"role": "system", "content": system_msg}]
        self.sliding_window_pairs = sliding_window_pairs

    def translate_document(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        chunk_size: int,
        retries: int = 3,
    ) -> Optional[str]:
        """
        Translate a whole document by adding its chunks to the chat
        and returning the reassembled translation.
        Returns None on failure after all retries.
        """
        chunks_meta = split_into_chunks(text, chunk_size)
        translated_parts: List[str] = []
        continuation_flags: List[bool] = []

        for i, (chunk_text, is_cont) in enumerate(chunks_meta, 1):
            # Append user message for this chunk
            self.messages.append({"role": "user", "content": chunk_text})
            saved_len = len(self.messages)  # so we can roll back on error

            success = False
            for attempt in range(1, retries + 1):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.messages,
                        temperature=0.1,
                    )
                    translation = response.choices[0].message.content.strip()
                    self.messages.append(
                        {"role": "assistant", "content": translation}
                    )
                    self._trim_messages()  # enforce sliding window
                    translated_parts.append(translation)
                    continuation_flags.append(is_cont)
                    success = True
                    break
                except Exception as e:
                    logger.warning(
                        f"Chunk {i}/{len(chunks_meta)} attempt {attempt}: {e}"
                    )
                    # Roll back to before this user message
                    self.messages = self.messages[:saved_len]
                    if attempt == retries:
                        logger.error("All retries exhausted for this chunk.")
                        return None
                    time.sleep(2**attempt)
            if not success:
                return None  # shouldn't be reached, but safety

        return reassemble_parts(translated_parts, continuation_flags)

    def _trim_messages(self):
        """Keep only system message + last N user‑assistant pairs."""
        if self.sliding_window_pairs <= 0:
            self.messages = [self.messages[0]]
            return
        # Exclude system, keep last 2*N messages (user+assistant pairs)
        tail = self.messages[1:]
        max_tail = 2 * self.sliding_window_pairs
        if len(tail) > max_tail:
            tail = tail[-max_tail:]
        self.messages = [self.messages[0]] + tail


# ----------------------------------------------------------------------
# Standalone file translation (for non‑serial mode)
# ----------------------------------------------------------------------
def translate_file_standalone(
    client: openai.OpenAI,
    input_path: Path,
    output_path: Path,
    source_lang: str,
    target_lang: str,
    model: str,
    chunk_size: int,
    retries: int = 3,
) -> bool:
    """
    Original per‑file translation with its own private chat session.
    No sliding window needed because a single chapter always fits.
    """
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            original_text = f.read()

        if not original_text.strip():
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text("", encoding="utf-8")
            logger.info(f"Skipped empty file: {input_path}")
            return True

        chunks_meta = split_into_chunks(original_text, chunk_size)
        logger.info(
            f"{input_path.name}: split into {len(chunks_meta)} chunks "
            f"(~{count_tokens(original_text)} tokens)"
        )

        system_msg = (
            f"Translate the following text from {source_lang} to {target_lang}. "
            "Preserve the original formatting, markdown, and special characters. "
            "Only return the translated text for each chunk, no extra commentary."
        )

        session = ChatSession(client, model, system_msg, sliding_window_pairs=0)
        # sliding_window_pairs=0 disables the window – keeps the whole conversation.
        # Actually we want it to keep everything (no trimming) for a single file.
        # So we'll set sliding_window_pairs to a very high number or just bypass.
        # We'll temporarily set it to a large value to prevent trimming.
        # Better: we can call _trim_messages with a huge number. We'll just not call it.
        # The session's translate_document always calls _trim_messages; we could pass
        # sliding_window_pairs=99999999 to effectively disable it. That's fine.
        session.sliding_window_pairs = 10**9  # effectively infinite

        translated = session.translate_document(
            original_text, source_lang, target_lang, chunk_size, retries
        )
        if translated is None:
            return False

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated)
        logger.info(f"Translated: {input_path} -> {output_path}")
        return True

    except Exception as e:
        logger.error(f"Failed to process {input_path}: {e}")
        if output_path.exists():
            output_path.unlink()
        return False


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Batch translate documents using DeepSeek API (or local Ollama)."
    )
    parser.add_argument(
        "--input-dir", required=True, help="Directory containing source documents"
    )
    parser.add_argument(
        "--output-dir", required=True, help="Directory to save translated documents"
    )
    parser.add_argument(
        "--source-lang", default="auto", help="Source language (default: auto)"
    )
    parser.add_argument(
        "--target-lang", default="English", help="Target language (default: English)"
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=[".txt", ".md", ".html", ".rst", ".xml"],
        help="File extensions to process",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=5,
        help="Number of parallel files (default: 5)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=3000,
        help="Max tokens per chunk (default: 3000)",
    )
    parser.add_argument(
        "--api-key", help="DeepSeek API key (or set DEEPSEEK_API_KEY env var)"
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Use local Ollama API (serial files, model gemma4:e4b)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re‑translate even if output file already exists",
    )
    parser.add_argument(
        "--serialize-all",
        action="store_true",
        help="Translate all files in a single chat session (book mode)",
    )
    parser.add_argument(
        "--sliding-window",
        type=int,
        default=16,
        help="Number of recent user‑assistant pairs to keep in serial mode (default: 16)",
    )

    args = parser.parse_args()

    # ---------- Local mode overrides ----------
    if args.local:
        base_url = LOCAL_BASE_URL
        args.model = LOCAL_MODEL
        args.max_workers = 1
        logger.info(
            f"Local mode: Ollama at {LOCAL_BASE_URL} with model '{LOCAL_MODEL}'"
        )
    else:
        base_url = DEEPSEEK_BASE_URL

    # ---------- API key ----------
    api_key = args.api_key or os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        if args.local:
            api_key = "ollama"  # dummy key
        else:
            logger.error(
                "DeepSeek API key not found. Provide --api-key or set DEEPSEEK_API_KEY."
            )
            sys.exit(1)

    client = openai.OpenAI(api_key=api_key, base_url=base_url)

    # ---------- Collect files ----------
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    if not input_dir.is_dir():
        logger.error(f"Input directory does not exist: {input_dir}")
        sys.exit(1)

    files_to_translate = []
    for ext in args.extensions:
        ext = ext if ext.startswith(".") else f".{ext}"
        files_to_translate.extend(input_dir.rglob(f"*{ext}"))
    files_to_translate = sorted(set(files_to_translate))
    logger.info(f"Found {len(files_to_translate)} files to translate.")
    if not files_to_translate:
        logger.info("Nothing to do. Exiting.")
        return

    # Build task list
    tasks = []
    for src_path in files_to_translate:
        rel_path = src_path.relative_to(input_dir)
        dst_path = output_dir / rel_path
        if dst_path.exists() and not args.force:
            logger.info(f"Skipping (already exists): {dst_path}")
            continue
        tasks.append((src_path, dst_path))

    if not tasks:
        logger.info("All files already translated. Exiting.")
        return

    # ---------- Serial‑all mode (book‑wide chat) ----------
    if args.serialize_all:
        logger.info(
            f"Book mode: serialising all {len(tasks)} files into one chat session. "
            f"Sliding window: {args.sliding_window} pairs."
        )
        # Build a system prompt suited for a whole book
        system_msg = (
            f"You are translating a document consisting of multiple files. "
            f"Translate each part from {args.source_lang} to {args.target_lang} "
            "with consistent style and terminology. "
            "Preserve formatting, markdown, and special characters. "
            "Only return the translated text, no extra commentary."
        )

        session = ChatSession(
            client,
            args.model,
            system_msg,
            sliding_window_pairs=args.sliding_window,
        )

        success_count = 0
        fail_count = 0
        for src_path, dst_path in tasks:
            logger.info(f"Processing {src_path.name} ...")
            try:
                with open(src_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except Exception as e:
                logger.error(f"Failed to read {src_path}: {e}")
                fail_count += 1
                continue

            translated = session.translate_document(
                text, args.source_lang, args.target_lang, args.chunk_size
            )
            if translated is None:
                logger.error(f"Translation failed for {src_path.name}")
                fail_count += 1
                if dst_path.exists():
                    dst_path.unlink()
                continue

            try:
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                dst_path.write_text(translated, encoding="utf-8")
                logger.info(f"Translated {src_path.name} → {dst_path}")
                success_count += 1
            except Exception as e:
                logger.error(f"Could not write {dst_path}: {e}")
                fail_count += 1

        logger.info(
            f"Book translation finished. Success: {success_count}, Failed: {fail_count}"
        )
        return

    # ---------- Normal parallel mode ----------
    logger.info(f"Parallel mode: {args.max_workers} workers.")
    success_count = 0
    fail_count = 0

    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        future_to_path = {
            executor.submit(
                translate_file_standalone,
                client,
                src,
                dst,
                args.source_lang,
                args.target_lang,
                args.model,
                args.chunk_size,
            ): src
            for src, dst in tasks
        }

        for future in as_completed(future_to_path):
            src = future_to_path[future]
            try:
                if future.result():
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                logger.error(f"Unexpected error for {src}: {e}")
                fail_count += 1

    logger.info(
        f"Translation complete. Success: {success_count}, Failed: {fail_count}"
    )


if __name__ == "__main__":
    main()
