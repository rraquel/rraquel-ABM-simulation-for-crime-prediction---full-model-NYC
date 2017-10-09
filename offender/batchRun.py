#!/bin/batchRun

for i in test1.ini test2.ini test3.ini default.ini; do
    offender/run.py $i &
    sleep 1
done
i in