#!/bin/bash
test agent number
for i in config/pretest3/* ; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done