LYX_HOME := /usr/share/lyx
TEX_HOME := $(shell kpsewhich -var-value=TEXMFHOME)
STY_DIR := $(TEX_HOME)/tex/latex/lecture-design

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

install:
	mkdir ~/.lyx/layouts/ -p
	cp lecture-design.module ~/.lyx/layouts/
	mkdir -p $(STY_DIR)
	cp lecture-design.sty $(STY_DIR)/
	python $(LYX_HOME)/configure.py

.PHONY: watch dev clean build
