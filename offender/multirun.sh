#!/bin/bash

#for i in config/perftest1/*.ini; do
for i in config/perftest1/*; do 
    offender/runOffender.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done
