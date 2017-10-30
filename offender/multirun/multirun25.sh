#!/bin/bash


for i in config25/* ; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done



 # ./multirun.sh |at now + 7 hours
  