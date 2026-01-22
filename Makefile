watch:
	find -path "./src/*.sty" \
		-or -name "*.tex" \
		-or -name "build.py" \
		-or -name "Makefile" | entr make pdf

pdf:
	make build
	texfot latexmk -pdf -interaction=nonstopmode sample.tex

view: lecture-design.sty
	latexmk -pdf -pvc sample.tex

build:
	python build.py src/main.sty -o lecture-design.sty

clean:
	latexmk -C
	rm -f lecture-design.sty

.PHONY: watch dev clean build
