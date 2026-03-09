#!/bin/sh

pandoc CHAPTERS/*.md PAPERS/*.md --toc --epub-cover-image=COVER/FRONT.jpg -o output.epub

