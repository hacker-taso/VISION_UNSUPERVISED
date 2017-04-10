#!/bin/sh
k=3
while [ $k -lt 16 ]; do python direct_cycle.py $k >> ../results/direct_cycle_result.txt; k=$((k+1)); done
k=20; python direct_cycle.py $k >> ../results/direct_cycle_result.txt
k=25; python direct_cycle.py $k >> ../results/direct_cycle_result.txt
k=30; python direct_cycle.py $k >> ../results/direct_cycle_result.txt
k=50; python direct_cycle.py $k >> ../results/direct_cycle_result.txt
