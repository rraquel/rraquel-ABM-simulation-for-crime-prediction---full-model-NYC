#!/bin/bash

#list=[]
#to run: in pythonprototype folder: bash offender/multirun/multirun.sh



#for i in default.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 100
#done
#ssd



#runs 2
for i in config/test1000_new/10/1000_s*.ini ; do 
    python3 offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done

#runs 2
for i in config/test1000_new/10/1000_u*.ini ; do 
    python3 offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done

#runs 11
#for i in config/test1000_new/10/1000_c*.ini ; do 
#    python3 offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 10
#done


  # starte zweite Ladung
#  offender/run.py