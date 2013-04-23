#!/bin/sh

cd src
pyflakes .
if [ $? -eq 2 ]; then exit 2; fi
pep8 .
./trader.py && ./test_trader.py && ./test_plugins.py
failure=$?
cd ..
if [ $failure -ne 0 ]; then exit $failure; fi
cd doc
lacheck report1.tex
failure=$?
cd ..
exit $failure
