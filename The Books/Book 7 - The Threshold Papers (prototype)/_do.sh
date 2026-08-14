#!/bin/bash

# Loop through all subdirectories in the current directory
# The */ pattern matches only directories; trailing slash avoids matching files
for dir in */ ; do
	# Remove the trailing slash to get the clean directory name
	dirname="${dir%/}"
	
	# Skip if no match (when no directories exist, the pattern remains as "*/")
	# Check if the entry actually exists and is a directory
	if [[ -d "$dirname" ]]; then
		echo "Processing language: $dirname"
		
		echo "Translating"
		if [[ "$dirname" != "en-us" ]]; then
			./_translate_$dirname.sh
		else
			echo "Skipping 'en-us' folder (blocked)."
		fi
	
	pandoc -o "$dirname.epub" $dirname/*.md --epub-cover-image=$dirname/cover.jpg
	
	pandoc -o "$dirname.txt" $dirname/*.md
	
	pandoc -o "$dirname.4_6.pdf" $dirname/*.md \
		--toc --toc-depth=2 \
		--pdf-engine=xelatex \
		-V documentclass=book \
		-V classoption=twoside \
		-V header-includes="\usepackage{fontspec}\setsansfont{Helvetica}\usepackage{sectsty}\allsectionsfont{\sffamily}" \
		-V geometry:"paperwidth=4in, paperheight=6in, inner=0.4in, outer=0.4in, top=0.5in, bottom=0.4in, bindingoffset=0in" \
		-V fontsize="10pt" \
		-V mainfont="Times New Roman" \
		-V mainfontoptions:LetterSpace=0
#		-V sansfont="Helvetica Neue" \
	
	pandoc -o "$dirname.55_85.pdf" $dirname/*.md \
		--toc --toc-depth=2 \
		--pdf-engine=xelatex \
		-V documentclass=book \
		-V classoption=twoside \
		-V header-includes="\usepackage{fontspec}\setsansfont{Helvetica}\usepackage{sectsty}\allsectionsfont{\sffamily}" \
		-V geometry:"paperwidth=5.5in, paperheight=8.5in, inner=0.5in, outer=0.5in, top=0.6in, bottom=0.5in, bindingoffset=0in" \
		-V fontsize="11pt" \
		-V mainfont="Times New Roman" \
		-V mainfontoptions:LetterSpace=0 \
#		-V sansfont="Helvetica Neue" \
		
	pdfbook2 -snp letterpaper -o 0 -i 0 -t 0 -b 0 "$dirname.55_85.pdf" 
	
	pandoc -o "$dirname.7_85.pdf" $dirname/*.md \
		--toc --toc-depth=2 \
		--pdf-engine=xelatex \
		-V documentclass=book \
		-V classoption=twoside \
		-V header-includes="\usepackage{fontspec}\setsansfont{Helvetica}\usepackage{sectsty}\allsectionsfont{\sffamily}" \
		-V geometry:"paperwidth=7in, paperheight=8.5in, inner=0.5in, outer=0.5in, top=0.6in, bottom=0.5in, bindingoffset=0in" \
		-V fontsize="11pt" \
		-V mainfont="Times New Roman" \
		-V mainfontoptions:LetterSpace=0 \
#		-V sansfont="Helvetica Neue" \
		
	pdfbook2 -snp legalpaper -o 0 -i 0 -t 0 -b 0 "$dirname.7_85.pdf" 
	
	pandoc -o "$dirname.pocket.pdf" $dirname/*.md \
		--toc --toc-depth=2 \
		--pdf-engine=xelatex \
		-V documentclass=book \
		-V classoption=twoside \
		-V header-includes="\usepackage{fontspec}\setsansfont{Helvetica}\usepackage{sectsty}\allsectionsfont{\sffamily}" \
		-V geometry:"paperwidth=4.25in, paperheight=6.875in, inner=0.5in, outer=0.5in, top=0.6in, bottom=0.5in, bindingoffset=0.125in" \
		-V fontsize="10pt" \
		-V mainfont="Times New Roman" \
		-V mainfontoptions:LetterSpace=0
#		-V sansfont="Helvetica Neue" \
		
	pandoc -o "$dirname.trade.pdf" $dirname/*.md \
		--toc --toc-depth=2 \
		--pdf-engine=xelatex \
		-V documentclass=book \
		-V classoption=twoside \
		-V header-includes="\usepackage{fontspec}\setsansfont{Helvetica}\usepackage{sectsty}\allsectionsfont{\sffamily}" \
		-V geometry:"paperwidth=6in, paperheight=9in, inner=0.75in, outer=0.75in, top=0.75in, bottom=0.75in, bindingoffset=0.175in" \
		-V fontsize="11pt" \
		-V mainfont="Times New Roman" \
		-V mainfontoptions:LetterSpace=0
#		-V sansfont="Helvetica Neue" \
		
	pandoc -o "$dirname.letter.pdf" $dirname/*.md \
		--toc --toc-depth=2 \
		--pdf-engine=xelatex \
		-V documentclass=book\
		-V classoption=twoside \
		-V header-includes="\usepackage{fontspec}\setsansfont{Helvetica}\usepackage{sectsty}\allsectionsfont{\sffamily}" \
		-V geometry:"paperwidth=8.5in, paperheight=11in, inner=1in, outer=1in, top=1in, bottom=1in, bindingoffset=0.25in" \
		-V fontsize="12pt" \
		-V mainfont="Times New Roman" \
		-V mainfontoptions:LetterSpace=0
#		-V sansfont="Helvetica" \
	else
		# No directories found – you can handle that case or exit silently
		echo "No directories found in the current location."
		break
	fi
done
