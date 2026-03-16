#!/bin/sh

# FE First Edition

edition="FE"

pandoc WARNING_EN/CHAPTERS/*.md WARNING_EN/PAPERS/*.md -s --toc --toc-depth=1 --epub-cover-image=WARNING_EN/COVER/FRONT.jpg -o "WarNing_($edition)_english.epub" 
pandoc WARNING_EN/CHAPTERS/*.md WARNING_EN/PAPERS/*.md -s -o "WarNing_($edition)_english.html"
pandoc WARNING_EN/CHAPTERS/*.md WARNING_EN/PAPERS/*.md -s -o "WarNing_($edition)_english.txt"
pandoc WARNING_EN/CHAPTERS/*.md WARNING_EN/PAPERS/*.md -s -o "WarNing_($edition)_english(booklet).pdf" --pdf-engine=weasyprint --toc --toc-depth=1 --css style_pdf_booklet.css
pandoc WARNING_EN/CHAPTERS/*.md WARNING_EN/PAPERS/*.md -s -o "WarNing_($edition)_english(letter).pdf" --pdf-engine=weasyprint --toc --toc-depth=1 --css style_pdf_letter.css

pandoc WARNING_FR/CHAPTERS/*.md WARNING_FR/PAPERS/*.md -s --toc --toc-depth=1 --epub-cover-image=WARNING_FR/COVER/FRONT.jpg -o "WarNing_($edition)_francais.epub"
pandoc WARNING_FR/CHAPTERS/*.md WARNING_FR/PAPERS/*.md -s -o "WarNing_($edition)_francais.html"
pandoc WARNING_FR/CHAPTERS/*.md WARNING_FR/PAPERS/*.md -s -o "WarNing_($edition)_francais.txt"
pandoc WARNING_FR/CHAPTERS/*.md WARNING_FR/PAPERS/*.md -s -o "WarNing_($edition)_francais(booklet).pdf" --pdf-engine=weasyprint --toc --toc-depth=1 --css style_pdf_booklet.css
pandoc WARNING_FR/CHAPTERS/*.md WARNING_FR/PAPERS/*.md -s -o "WarNing_($edition)_francais(lettre).pdf" --pdf-engine=weasyprint --toc --toc-depth=1 --css style_pdf_letter.css

