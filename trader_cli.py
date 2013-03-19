"""Trader command line interface"""

from trader import run_trial
import sys

def main():
    """Run the trial, taking market data from stdin"""
    run_trial(sys.stdin)

if __name__ == '__main__':
    main()
