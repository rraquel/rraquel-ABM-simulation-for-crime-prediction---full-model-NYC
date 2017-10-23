#!/bin/bash

#for i in config/perftest1/*.ini; do
for i in config/pretest1/test1.ini config/pretest1/test2.ini config/pretest1/test3.ini config/pretest1/test4.ini config/pretest1/test5.ini; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done
