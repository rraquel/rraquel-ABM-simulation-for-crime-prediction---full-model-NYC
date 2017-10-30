#!/bin/bash

#list=[]
#to run: in pythonprototype folder: bash offender/multirun.sh




########### first batch ###############
for i in config/pretest114/test1.ini config/pretest114/test2.ini config/pretest114/test3.ini config/pretest114/test4.ini config/pretest114/test5.ini config/pretest114/test6.ini config/pretest114/test7.ini config/pretest114/test8.ini config/pretest114/test9.ini ; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done

############second batch ###############

#for i in config/pretest114/test10.ini config/pretest114/test11.ini config/pretest114/test12.ini config/pretest114/test13.ini config/pretest114/test14.ini config/pretest114/test15.ini config/pretest114/test16.ini config/pretest114/test17.ini config/pretest114/test18.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 1
#done


 # ./multirun.sh |at now + 7 hours
  