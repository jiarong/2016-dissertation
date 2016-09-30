#Makefile for pdflatex

PROJECT=main
TEX=pdflatex
BIBTEX=bibtex

all: $(PROJECT).pdf

$(PROJECT).pdf: $(PROJECT).tex
	$(TEX) $(PROJECT).tex
	$(BIBTEX) $(PROJECT)
	$(TEX) $(PROJECT).tex
	$(TEX) $(PROJECT).tex

clean-all:
	rm -f *.dvi *.log *.bak *.aux *.bbl *.blg *.idx *.ps *.eps *.pdf *.toc *.out *~

clean:
	rm -f *.log *.bak *.aux *.bbl *.blg *.idx *.toc *.out *~
