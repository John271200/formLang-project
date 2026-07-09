# Compilation des fiches (pdflatex, 2 passes pour les en-têtes)
TEX := $(wildcard jour*.tex)
PDF := $(TEX:.tex=.pdf)
all: $(PDF)
%.pdf: %.tex iutparakou.sty
	pdflatex -interaction=nonstopmode -halt-on-error $<
	pdflatex -interaction=nonstopmode -halt-on-error $<
clean:
	rm -f *.aux *.log *.out *.toc
.PHONY: all clean
