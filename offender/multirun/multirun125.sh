#!/bin/bash



while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 1 ]; then
    # starte zweite Ladung
    for i in config/test/125/test125PPV.ini config/test/125/test125PRR.ini; do 
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
    for i in config/test/125/test125SPV config/test/125/test125SRV; do 
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
    for i in config/test/125/test125**; do 
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
    for i in config/test/125/test125**; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done
    break
  fi
  sleep 600
done


 # ./multirun.sh |at now + 7 hours
  