#!/bin/batchRun
#for i in test1.ini test2.ini test3.ini default.ini; do
for i in config/test1.ini, config/test2.ini:
    offender/run.py