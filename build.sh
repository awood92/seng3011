#!/bin/sh

cd src
pyflakes .
if [ $? -eq 2 ]; then exit 2; fi
pep8 .
py_compilefiles *.py plugins/*.py && pydoc -w trader trader_cli test_trader plugins test_plugins && ./trader.py && ./test_trader.py && ./test_plugins.py
failure=$?
cd ..
if [ $failure -ne 0 ]; then exit $failure; fi
cd doc
lacheck report1.tex && pdflatex report1.tex && rm -f report1.zip && zip report1 report1.pdf
failure=$?
cd ..
exit $failure