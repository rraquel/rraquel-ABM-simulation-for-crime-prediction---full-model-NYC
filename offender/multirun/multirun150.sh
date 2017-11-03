#!/bin/bash



while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 1 ]; then
    # starte zweite Ladung
    for i in config/runStatic/1/test150*; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 100
done
    break
  fi
  sleep 600
done

while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 1 ]; then
    # starte zweite Ladung
    for i in config/runPower/2/test150*; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 100
done
    break
  fi
  sleep 600
done


while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 1 ]; then
    # starte zweite Ladung
    for i in config/runStatic/2/test150*; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 100
done
    break
  fi
  sleep 600
done

while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 1 ]; then
    # starte zweite Ladung
    for i in config/runPower/1/test150*; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 100
done
    break
  fi
  sleep 600
done


 # ./multirun.sh |at now + 7 hours
  