#!/bin/sh
k=10
while [ $k -lt 13 ]; do python ../advanced/undirected_cycle.py $k >> ../results/undirected_cycle_result.txt; k=$((k+1)); done

