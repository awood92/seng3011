#!/bin/sh

python -m SimpleHTTPServer & ./src/trader_gui.py && killall python
