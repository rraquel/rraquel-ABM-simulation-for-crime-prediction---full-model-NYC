#!/bin/bash

#list=[]
#to run: in pythonprototype folder: bash offender/multirun.sh

#for i in config/perftest1/*.ini; do
for i in config/pretest/test1.ini config/pretest/test2.ini config/pretest/test3.ini config/pretest/test4.ini config/pretest/test5.ini config/pretest/test6.ini config/pretest/test7.ini config/pretest/test8.ini config/pretest/test9.ini ; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done

#offender/run.py blubb.ini | at now + 7 hours

while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [$NUMPROCS -le 1]; then
    # starte zweite Ladung
    for i in config/pretest/test10.ini config/pretest/test11.ini config/pretest/test12.ini config/pretest/test13.ini config/pretest/test14.ini config/pretest/test15.ini config/pretest/test16.ini config/pretest/test17.ini config/pretest/test18.ini ; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done
    break
  fi
  sleep 10
done
  
 # ./multirun.sh |at now + 7 hours
  