#!/bin/bash

#list=[]
#to run: in pythonprototype folder: bash offender/multirun.sh



#for i in config/numAgents/test25* config/numAgents/test100* ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 100
#done

while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 4 ]; then
    # starte zweite Ladung
    offender/run.py
    sleep 10
done
    break
  fi
  sleep 10
done





 # ./multirun.sh |at now + 7 hours
  