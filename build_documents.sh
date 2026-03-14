#!/bin/sh

pandoc WARNING_EN/CHAPTERS/*.md WARNING_EN/PAPERS/*.md -s --toc --epub-cover-image=WARNING_EN/COVER/FRONT.jpg -o WarNing_english.epub
pandoc WARNING_EN/CHAPTERS/*.md WARNING_EN/PAPERS/*.md -s -o WarNing_english.html
pandoc WARNING_EN/CHAPTERS/*.md WARNING_EN/PAPERS/*.md -s -o WarNing_english.md
pandoc WARNING_EN/CHAPTERS/*.md WARNING_EN/PAPERS/*.md -s -o WarNing_english.pdf --pdf-engine=weasyprint --css style_pdf_6x9.css

pandoc WARNING_FR/CHAPTERS/*.md WARNING_FR/PAPERS/*.md -s --toc --epub-cover-image=WARNING_FR/COVER/FRONT.jpg -o WarNing_francais.epub
pandoc WARNING_FR/CHAPTERS/*.md WARNING_FR/PAPERS/*.md -s -o WarNing_francais.html
pandoc WARNING_FR/CHAPTERS/*.md WARNING_FR/PAPERS/*.md -s -o WarNing_francais.md
pandoc WARNING_FR/CHAPTERS/*.md WARNING_FR/PAPERS/*.md -s -o WarNing_francais.pdf --pdf-engine=weasyprint --css style_pdf_6x9.css

