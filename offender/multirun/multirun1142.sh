#!/bin/bash

#list=[]
#to run: in pythonprototype folder: bash offender/multirun.sh




########### first batch ###############


############second batch ###############

############second batch ###############
for i in config/pretest114/test10.ini config/pretest114/test11.ini config/pretest114/test12.ini config/pretest114/test13.ini config/pretest114/test14.ini config/pretest114/test15.ini config/pretest114/test16.ini config/pretest114/test17.ini config/pretest114/test18.ini ; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done

 # ./multirun.sh |at now + 7 hours
  