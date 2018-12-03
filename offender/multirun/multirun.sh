#!/bin/bash

#list=[]
#to run: in pythonprototype folder: bash offender/multirun/multirun.sh



#for i in default.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 100
#done
#ssd



#runs 1
for i in config/test1000_new/all/1000_ct6*.ini ; do 
    python3 offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 100
done

for i in config/test1000_new/all/1000_ct2*.ini ; do 
    python3 offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 100
done
for i in config/test1000_new/all/1000_ct1_*.ini ; do 
    python3 offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 100
done




#for i in config/test1000_new/2/*.ini ; do 
#    python3 offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 100
#done


  # starte zweite Ladung
#  offender/run.py