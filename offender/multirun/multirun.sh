#!/bin/bash

#list=[]
#to run: in pythonprototype folder: bash offender/multirun.sh



for i in config/default.ini ; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 100
done

  # starte zweite Ladung
#  offender/run.py