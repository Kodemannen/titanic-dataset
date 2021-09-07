#!/bin/sh

cd report
pdflatex report.tex
cd -
#bibtex math_notes.aux
#pdflatex math_notes.tex
#pdflatex math_notes.tex
#echo report compiled
