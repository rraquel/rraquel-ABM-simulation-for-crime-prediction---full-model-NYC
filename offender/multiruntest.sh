#!/bin/bash

#list=[]
#to run: in pythonprototype folder: python3 offender/multirun.sh

#for i in config/perftest1/*.ini; do
for i in config/pretest/test1.ini config/pretest/test2.ini ; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done