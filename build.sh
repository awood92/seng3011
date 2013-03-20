#!/bin/sh

echo "aoeuaoeuaoeuaoeuaoeu"
pycompile *.py && pydoc -w trader trader_cli test_trader && ./trader.py && ./test_trader.py && pdflatex -output-directory doc doc/report1.tex
echo "aoeuaoeuaoeuaoeuaoeu"
