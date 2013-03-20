#!/bin/sh

pycompile *.py && pydoc -w trader trader_cli test_trader && ./trader.py && ./test_trader.py
