#!/bin/bash

#list=[]
#to run: in pythonprototype folder: q



#for i in default.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 100
#done
#ssd

for i in config/test1000_new/7/1000_td_*.ini ; do 
    python3 offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 100
done


#for i in config/test1000_new/2/*.ini ; do 
#    python3 offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 100
#done


  # starte zweite Ladung
#  offender/run.py