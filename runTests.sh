#!/bin/sh

cd src
#pyflakes .
if [ $? -eq 2 ]; then exit 2; fi
#pep8 .
py_compilefiles *.py plugins/*.py && pydoc -w trader trader_cli test_trader plugins test_plugins && ./test_trader.py && ./test_plugins.py
echo "\n\n---------------------------------TESTINFO----------------------------------"
# Putting test info in 1 file, later i'll create testinfo files for each of the tests, and it'll print it before each test - Chris
cat "../sample/testinfo"
echo "\n---------------------------------------------------------------------------"
for f in ../sample/test*.csv
  do
    echo "Running $f\n"
    orderlist=`cat $f | ./trader_cli.py -e "Initial Engine" -s "Initial Strategy Evaluator" -g "Initial Signal Generator"`
    # comment both lines below to remove trade count - Chris
    echo "TRADES: "
    echo `echo "$orderlist" | grep "TRADE" -c`
    # comment line below to remove tradelist  - Chris
    echo "\n$orderlist"
    echo "---------------------------------------------------------------------------"
done
failure=$?
cd ..
if [ $failure -ne 0 ]; then exit $failure; fi
cd doc
#lacheck report1.tex && pdflatex report1.tex && rm -f report1.zip && zip report1 report1.pdf
failure=$?
cd ..
exit $failure
