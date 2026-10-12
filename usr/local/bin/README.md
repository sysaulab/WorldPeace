# Book Pipeline

A small toolchain for turning a directory of Markdown chapters into ebooks (EPUB), print-ready PDFs (trade and pocket formats), plain text, translated editions, and per-chapter audiobooks.

The three scripts share a single `book.json` config file at the project root and a simple naming convention for chapter files:

```
NNNN - Title.md
```

This gives stable sort order and readable filenames.

---

## What each script does

| Script | Purpose |
| --- | --- |
| `mkbook.py` | Builds EPUB, plain text, and one or more PDF formats from `{lang}/*.md`. Optionally invokes the translator first. |
| `translate.py` | Batch-translates a source language directory into a target language directory using the DeepSeek API (or a local Ollama model). |
| `mkaudiobook.py` | Strips Markdown to prose and synthesizes one M4A per chapter using `say`, `piper`, or `espeak-ng`. Also writes the cleaned prose as `.txt`. |

`mkbook.py` shells out to a translation command (`translate_cmd`) for any non-source language it builds — so you don't have to run `translate.py` by hand.

---

## Directory layout

The pipeline is driven entirely by `book.json` plus a directory per language. A typical project looks like this:

```
mybook/
├── book.json                # config — everything below is driven by this
├── translate.py
├── mkbook.py
├── mkaudiobook.py
├── deepseek_tokenizer.py    # required by translate.py
│
├── en/                      # source language (source_lang in book.json)
│   ├── metadata.yaml        # Pandoc metadata (title, author, date, …)
│   ├── cover.jpg            # used as EPUB cover
│   ├── 0001 - A Beginning.md
│   ├── 0002 - The Road.md
│   ├── 0003 - Arrival.md
│   └── …
│
├── es/                      # target language (auto-generated)
│   ├── metadata.yaml
│   ├── cover.jpg
│   ├── 0001 - A Beginning.md
│   └── …
│
└── fr/
    └── …
```

Rules:

- **One directory per language**, named after the language *code* used in `book.json`.
- **`source_lang`** names the directory that is authoritative. Its files are never overwritten by the translator.
- **Every other directory listed in `languages`** is treated as a translation target if it doesn't exist yet, and rebuilt from source when it does.
- **Chapter files must be Markdown (`*.md`)** and sort into the reading order you want. Leading zero-padded numbers (e.g. `0001`) are the simplest way to achieve this.
- **`metadata.yaml`** and **`cover.jpg`** are per-language and optional, but recommended — they populate the title page and EPUB cover.
- **Audiobook output goes under `{lang}/audio/`**:
  ```
  {lang}/audio/m4a/NNNN - Title.m4a
  {lang}/audio/text/NNNN - Title.txt
  ```

You can keep everything in one repo. Generated artifacts (`.epub`, `.pdf`, `.txt`, and the `audio/` subfolders) are safe to `.gitignore`.

---

## Installing

```bash
# Python
pip install openai tiktoken

# System tools (Debian/Ubuntu examples; adjust for macOS/brew)
sudo apt install pandoc ffmpeg espeak-ng
# For print PDFs with imposition: pdfbook2 (from texlive-extra-utils)
sudo apt install texlive-extra-utils
```

`translate.py` also needs the small helper it imports:

```python
# deepseek_tokenizer.py
from tokenizers import Tokenizer
_tokenizer = Tokenizer.from_pretrained("deepseek-ai/DeepSeek-V3")
ds_token = _tokenizer
```

(or any module that exposes `ds_token.encode(...)` — it's only used to count tokens for chunking).

macOS users get `say` for free; `piper` is an optional offline neural TTS engine you can install separately.

---

## Example `book.json`

Here is a full working config with **trade** (6″×9″) and **pocket** (A-format, 4.25″×6.87″) print formats baked in. Save as `book.json` in the project root.

```json
{
  "source_lang": "en",

  "languages": {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German"
  },

  "translate_cmd": "./translate.py",

  "epub": {
    "cover_image": "cover.jpg"
  },

  "pdf": {
    "engine": "xelatex",
    "documentclass": "book",
    "classoption": "openany,oneside",
    "header_includes": "\\usepackage{microtype}\\usepackage{fontspec}",
    "mainfont": "EB Garamond",
    "mainfontoptions": "Numbers=OldStyle",
    "toc": true,
    "toc_depth": 2,

    "outputs": [
      {
        "name": "trade",
        "width": "6in",
        "height": "9in",
        "inner": "0.875in",
        "outer": "0.625in",
        "top": "0.75in",
        "bottom": "0.75in",
        "bindingoffset": "0.125in",
        "fontsize": "11pt"
      },
      {
        "name": "pocket",
        "width": "4.25in",
        "height": "6.87in",
        "inner": "0.5in",
        "outer": "0.375in",
        "top": "0.5in",
        "bottom": "0.5in",
        "bindingoffset": "0.125in",
        "fontsize": "9pt",
        "impose_paper": "a4"
      }
    ]
  },

  "audio": {
    "engine": "say",
    "rate": 175,
    "bitrate": "64k",
    "sample_rate": 22050,
    "voice": {
      "en": "Samantha",
      "es": "Mónica",
      "fr": "Amélie",
      "de": "Anna"
    }
  }
}
```

### Notes on the two print formats

- **`trade`** is a standard 6″×9″ trade paperback with a wider inner margin for the spine. No imposition is applied — you feed the resulting PDF straight to your print-on-demand service (KDP, IngramSpark, Lulu, etc.).
- **`pocket`** is roughly A-format (4.25″×6.87″), tighter margins, smaller type, and it sets `impose_paper` — so after Pandoc produces the PDF, `pdfbook2` will impose it 2-up on A4 sheets for at-home booklet printing. Remove `impose_paper` if you're sending it to a commercial printer.

The `mainfont` (`EB Garamond` above) must be installed on the machine. On macOS, `Times New Roman` or `Palatino` are safe defaults. With `xelatex` you can use any font by name.

---

## Building

Everything is run from the project root (where `book.json` lives).

### Books

```bash
# Build every language defined in book.json (translating as needed)
./mkbook.py

# Build just one language
./mkbook.py -l es

# Skip translation — build only what's already on disk
./mkbook.py --no-translate

# Use a different config file
./mkbook.py -c alternate-book.json
```

Outputs land next to each language directory:

```
en.epub
en.txt
en.trade.pdf
en.pocket.pdf       # imposed on A4 if impose_paper is set
```

### Translation only

`translate.py` is a standalone tool. `mkbook.py` calls it with these arguments, so you rarely need to run it directly:

```bash
./translate.py \
  --input-dir en \
  --output-dir es \
  --source-lang English \
  --target-lang Spanish
```

Useful flags:

```bash
# Parallel workers (default 5)
--max-workers 8

# Max tokens per chunk (default 3000)
--chunk-size 4000

# Use a local Ollama model instead of DeepSeek
--local

# Translate the whole book in one chat session for consistent terminology
--serialize-all --sliding-window 24

# Re-translate even if the output file already exists
--force
```

Set `DEEPSEEK_API_KEY` in your environment, or pass `--api-key`.

### Audiobooks

```bash
# Text-only pass (fast; writes {lang}/audio/text/*.txt without synthesizing)
./mkaudiobook.py --text-only

# Synthesize all languages
./mkaudiobook.py

# One language, re-doing cached chapters
./mkaudiobook.py -l en --force
```

Switching engines: set `audio.engine` in `book.json`.

- **`say`** (default on macOS) — zero setup, uses installed system voices.
- **`piper`** — offline neural TTS; set `audio.piper_bin` and `audio.piper_models` (a `{lang: /path/to/model.onnx}` map).
- **`espeak-ng`** — pragmatic Linux fallback; no configuration beyond `audio.voice`.

`ffmpeg` is required for transcoding to M4A regardless of engine.

---

## A worked end-to-end example

```bash
# 1. Write chapters in English (source language)
mkdir -p en
$EDITOR en/0001\ -\ A\ Beginning.md
$EDITOR en/0002\ -\ The\ Road.md
# … plus en/metadata.yaml and en/cover.jpg

# 2. Create book.json (see example above)

# 3. Build English EPUB + PDFs + plain text
./mkbook.py -l en --no-translate

# 4. Translate to Spanish, then build Spanish outputs
export DEEPSEEK_API_KEY=sk-…
./mkbook.py -l es

# 5. Generate the English audiobook
./mkaudiobook.py -l en
```

Result:

```
en.epub
en.txt
en.trade.pdf
en.pocket.pdf
en/audio/m4a/0001 - A Beginning.m4a
en/audio/m4a/0002 - The Road.m4a
en/audio/text/0001 - A Beginning.txt
en/audio/text/0002 - The Road.txt
es.epub
es.trade.pdf
es.pocket.pdf
…
```

---

## Config reference

### Top level

| Key | Required | Meaning |
| --- | --- | --- |
| `source_lang` | yes | Language code of the authoritative directory. |
| `languages` | yes | Map of language code → full language name (used by the translator). |
| `translate_cmd` | no | Path to the translator. Defaults to `translate`. |
| `epub` | no | `{ "cover_image": "cover.jpg" }` — relative to each language directory. |
| `pdf` | yes | See below. |
| `audio` | no | See below. |

### `pdf`

| Key | Meaning |
| --- | --- |
| `engine` | Pandoc PDF engine (`xelatex`, `lualatex`, `wkhtmltopdf`, …). |
| `documentclass`, `classoption` | LaTeX class and options. |
| `header_includes` | Raw LaTeX injected into the preamble. |
| `mainfont`, `mainfontoptions` | Font family and options (xelatex/lualatex only). |
| `toc`, `toc_depth` | Whether to insert a table of contents. |
| `outputs[]` | One entry per PDF format to produce. |

Each entry in `pdf.outputs[]`:

| Key | Meaning |
| --- | --- |
| `name` | Suffix in the output filename: `{lang}.{name}.pdf`. |
| `width`, `height` | Trim size. |
| `inner`, `outer`, `top`, `bottom` | Margins. `inner`/`outer` are swapped on even pages by `geometry`. |
| `bindingoffset` | Extra gutter allowance. |
| `fontsize` | Base type size. |
| `impose_paper` | Optional. If set (e.g. `"a4"`, `"letter"`), runs `pdfbook2` to impose the output. |

### `audio`

| Key | Meaning |
| --- | --- |
| `engine` | `say`, `piper`, or `espeak`. |
| `rate` | Words per minute (say) or speed (espeak). |
| `voice` | Either a string (same voice for all) or a `{lang: voice}` map. |
| `bitrate`, `sample_rate` | Passed to `ffmpeg` when transcoding to M4A. |
| `piper_bin` | Path/name of the `piper` executable. |
| `piper_models` | `{lang: /path/to/model.onnx}` map for piper. |

# Installation (UNIX)

Copy the files to /usr/local/bin and remove the trailing .py. Use "chmod +x" on each file to make them executable, and export the API key to have access to the translate functionality.

---

## Tips

- **Keep chapter filenames stable.** The translator writes to the same relative path in the target language, and `mkaudiobook.py` uses the stem for its output names. Renaming a chapter in `en/` means it'll be re-translated next run.
- **Don't hand-edit translated chapters** unless you're prepared to lose them: `mkbook.py` will overwrite them on the next build. If you need to hand-fix a translation, drop the corresponding file from the source directory into a scratch folder, or set `--no-translate` and edit only the target directory.
- **`--serialize-all` is for consistency, not speed.** It translates the whole book in one chat with a sliding window, which helps terminology and voice stay stable across chapters. It's much slower than the default parallel mode.
- **`--text-only` on `mkaudiobook.py`** is worth running first — it lets you proofread the prose without paying the synthesis cost.
- **Cross-platform fonts:** if `EB Garamond` isn't installed, the PDF build will fail loudly. Swap in `Times New Roman` or `Palatino` in `book.json` to get going quickly, then install a proper book font later.
