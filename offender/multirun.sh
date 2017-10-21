#!/bin/bash

#for i in config/perftest1/*.ini; do
for i in test1.ini test2.ini test3.ini test4.ini test5.ini; do 
    offender/runOffender.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done
