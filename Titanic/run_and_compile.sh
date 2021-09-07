#!/bin/sh

# we cd into this folder in the aliasin .bash_aliases

#pwd
python titanic_data_cleaning.py
cd report
pdflatex report.tex
cd -
#bibtex math_notes.aux
#pdflatex math_notes.tex
#pdflatex math_notes.tex
#echo report compiled
