#!/bin/bash


while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 3 ]; then
    # starte zweite Ladung
    for i in config/test25/1/*; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done
    break
  fi
  sleep 600
done

while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 3 ]; then
    # starte zweite Ladung
    for i in config/test25/2/*; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done
    break
  fi
  sleep 600
done

while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 3 ]; then
    # starte zweite Ladung
    for i in config/test25/3/*; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done
    break
  fi
  sleep 600
done

while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 3 ]; then
    # starte zweite Ladung
    for i in config/test25/4/*; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done
    break
  fi
  sleep 600
done






 # ./multirun.sh |at now + 7 hours
  