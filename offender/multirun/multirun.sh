#!/bin/bash

#list=[]
#to run: in pythonprototype folder: bash offender/multirun.sh



#for i in config/numAgents/test25* config/numAgents/test100* ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 100
#done

while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 3 ]; then
    # starte zweite Ladung
    for i in config/default.ini; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done
    break
  fi
  sleep 10
done





 # ./multirun.sh |at now + 7 hours
  