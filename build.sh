#!/bin/sh

cd src
success=false
if pycompile . && pydoc -w trader trader_cli test_trader && ./trader.py && ./test_trader.py
then success=true
fi
cd ..
if ! $success; then exit 1; fi
pdflatex -output-directory doc doc/report1.tex
