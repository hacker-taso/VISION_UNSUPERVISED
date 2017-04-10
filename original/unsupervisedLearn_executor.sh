#!/bin/sh
k=3
while [ $k -lt 16 ]; do python unsupervisedLearn.py $k >> ../results/unsupervisedLearn_result.txt; k=$((k+1)); done
k=20; python unsupervisedLearn.py $k >> ../results/unsupervisedLearn_result.txt
k=25; python unsupervisedLearn.py $k >> ../results/unsupervisedLearn_result.txt
k=30; python unsupervisedLearn.py $k >> ../results/unsupervisedLearn_result.txt
k=50; python unsupervisedLearn.py $k >> ../results/unsupervisedLearn_result.txt

