#!/bin/sh

cd src
#pyflakes .
if [ $? -eq 2 ]; then exit 2; fi
#pep8 .
py_compilefiles *.py plugins/*.py && pydoc -w trader trader_cli test_trader plugins test_plugins
echo "\n\n---------------------------------TESTINFO----------------------------------"
# Putting test info in 1 file, later i'll create testinfo files for each of the tests, and it'll print it before each test - Chris
echo "\n---------------------------------------------------------------------------"
cd ..
for f in sample/test[0-9].csv
  do
    echo "Running $f\n"
    outputfile=`echo $f | sed "s/\.csv/_filteroutput.tsv/g"`
    rubbishbin=`cat $f | ./src/trader_cli.py -e "Initial Engine" -s "Initial Strategy Evaluator" -g "Dummy Signal Generator"`
    difference=`cat ./evaluator/filter.tsv | diff $outputfile -`
    echo $difference
    difference=echo $difference | sed "s/ //"
    differences=$differences$difference
    echo "---------------------------------------------------------------------------"
done

differences=echo $differences | sed "s/ //"
if [ -n $differences ]; then echo "All tests passed"; else echo "Some tests failed"; fi
