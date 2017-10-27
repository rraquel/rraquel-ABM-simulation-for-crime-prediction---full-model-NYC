#!/bin/bash

for i in config/pretestMU/* ; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done