#!/bin/bash


while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 3 ]; then
    # starte zweite Ladung
    for i in config/test/125/test125SPVC.ini config/test/125/test125SRV.ini; do 
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
    for i in config/test/125/test125PRVC.ini config/test/125/test125SPV.ini; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done
    break
  fi
  sleep 600
done

while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 1 ]; then
    # starte zweite Ladung
    for i in config/test/125/test125SRR.ini config/test/125/test125UPVC.ini; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done
    break
  fi
  sleep 600
done

while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 1 ]; then
    # starte zweite Ladung
    for i in config/test/125/test12USRR.ini config/test/125/test125URVC.ini; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done
    break
  fi
  sleep 600
done



 # ./multirun.sh |at now + 7 hours
  