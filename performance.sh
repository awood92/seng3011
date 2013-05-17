#!/bin/sh

for f in $@; do
    for i in 'Dummy Signal Generator' 'Initial Signal Generator' 'Momentum Signal Generator' 'Mean Reversion Signal Generator'; do
        for j in 'Dummy Engine' 'Initial Engine'; do
            for k in 'Dummy Strategy Evaluator'; do
                time ./trader_cli.py -g"$i" -e"$j" -s"$k" <$f >out_$f
            done
        done
    done
done
