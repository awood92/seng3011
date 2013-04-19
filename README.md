SENG3011
========

Software Engineering Project Group 3:

* Nicholas Grasevski - Project Manager
* George El Boustani - Tester
* Daniel Morton - Programmer
* Christopher Tin Loi - Programmer

Sirca login details:

----
    user: demo3@demo
    pass: AD81631F
----

Requirements
------------
This is our progress on the functional requirements so far, for each requirement id:

1. We have completed this requirement. We simply read each row into a dictionary object, indexed by the field names specified in the first row of the CSV file.
2. We have implemented two trivial strategies so far - a dummy strategy which does nothing, and a strategy where the user presets a buy time and a sell time. The parameters for the latter strategy can be configured in `src/plugins/InitialSignalGenerator.yapsy-plugin`.
3. We have completed this requirement. We have implemented our simulation framework such that different strategies can be plugged in.
4. We have implemented two fully functional engine plugins so far - a dummy engine which does nothing, and a "matching without impact" engine, as per the assignment specification. Our next step is to implement a plugin with impact analysis.
5. We have implemented two trivial strategy evaluators so far - a dummy evaluator which does nothing, and an evaluator which outputs a basic report text file, listing the algorithmic trades made and the resultant profit/loss.
6. This is covered in the previous functional requirement.
7. We currently only have a command line interface.
8. We have not implemented this requirement yet.

And the quality requirements so far, for each requirement id:

1. The performance of our software is currently quite reasonable. We leverage the performance of the vast collection of standard Python libraries and data structures, so performance has not been a great issue.
2. We have not yet created a GUI, but usability aspects have been considered in our CLI. We have used the standard optparse library for command line option handling. We have also kept our program simple by primarily using standard input and output. This allows for easier use in batch scripts and pipelines.
3. We have not addressed this requirement yet.
4. Our strategy performance report is currently very basic, and we plan to improve this in the next prototype.

Installation
------------
Linux:

1. Extract this zip somewhere
2. `cd src`
3. Sample sirca files in `sample`

Windows:

1. Install Python
2. Same as Linux

Usage
-----
Our implementation consists of 3 main ingredients:

1. `src/trader_cli.py` - The main command line program
2. `sample/*.csv` - Sample historical data from Sirca
3. `src/plugins/*.py, src/plugins/*.yapsy-plugin` - Plugins, with their corresponding configuration files

The main command line program reads historical trading data (ie the Sirca file) in CSV format from standard input and outputs the resultant trades to standard output in the same CSV format. Various plugins can be chosen for the signal generator, engine and strategy evaluator by specifying these in the command line options, otherwise the default dummy plugins are used. Further usage help for the command line interface can be invoked as follows:

----
    ./trader_cli.py -h
----

There are 3 types of plugins:

1. Signal Generator - A strategy functor, which takes in trading data and outputs algorithmic orders
2. Engine - An engine functor, which takes in trading data and outputs trades
3. Strategy Evaluator - An evaluation function which takes in trades and outputs a report

These are stored in `src/plugins/`. Each plugin has a `.py` file with the implementation logic, and a `.yapsy-plugin` configuration file, with the parameters and other info. Currently the best way to change parameters is to edit the `.yapsy-plugin` file for the corresponding plugin. For example, if you wanted to change the buy and sell times for the "Initial Signal Generator", you could edit `src/plugins/InitialSignalGenerator.yapsy-plugin` and change the corresponding `buy_time` and `sell_time` variables. Then just save and rerun the program.

There are currently 6 plugins to choose from:

1. Dummy Signal Generator - the default signal generator. Takes in trading data and outputs no algorithmic orders.
2. Dummy Engine - the default engine. Takes in trading data and outputs no algorithmic trades.
3. Dummy Strategy Evaluator - the default strategy evaluator. Takes an array of trades and does nothing.
4. Initial Signal Generator - reads a buy time and a sell time (as well as price, volume etc) from the config file and outputs a corresponding buy and sell order, respectively.
5. Initial Engine - implements matching without impact, as per the requirements specification.
6. Initial Strategy Evaluator - takes an array of trades and writes a simple report to a file specified in the config file.

Example use cases:

----
    # Run trader simulation using dummy plugins which produce no output.
    # NOTE: trader_cli.py must be run from within the src directory, because
    # it refers to the "plugins" subdirectory!
    ./trader_cli.py <../sample/sample.csv

    # Run trader simulation using initial engine and initial strategy
    # evaluator, and output the trades to a file. Then read the report
    # outputted by the initial strategy evaluator.
    ./trader_cli.py -e'Initial Engine' -s'Initial Strategy Evaluator' <../sample/sample2.csv >trades.csv
    less Report.txt

    # Edit parameters for the Initial Signal Generator plugin, then run.
    vi plugins/InitialSignalGenerator.yapsy-plugin
    ./trader_cli.py -g'Initial Signal Generator' -e'Initial Engine' -s'Initial Strategy Evaluator' <../sample/sample.csv >trades.csv
    less Report.txt
----

See our black box testing scripts `runTests.sh` and `run.sh` for further use cases.
