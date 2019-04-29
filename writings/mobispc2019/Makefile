pdf:
	latexmk -pdf main

watch:
	latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" -pvc main

clean:
	latexmk -c
	rm -f main.pdf main.bbl
