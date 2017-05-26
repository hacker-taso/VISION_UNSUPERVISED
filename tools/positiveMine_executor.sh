#!/bin/sh
k=3
while [ $k -lt 16 ]; do python ../original/positiveMine.py $k >> ../results/positiveMine_result.txt; k=$((k+1)); done
k=20; python ../original/positiveMine.py $k >> ../results/positiveMine_result.txt
k=25; python ../original/positiveMine.py $k >> ../results/positiveMine_result.txt
k=30; python ../original/positiveMine.py $k >> ../results/positiveMine_result.txt
k=50; python ../original/positiveMine.py $k >> ../results/positiveMine_result.txt

