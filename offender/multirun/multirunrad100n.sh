#!/bin/bash

#list=[]
#to run: in pythonprototype folder: bash offender/multirun.sh



#for i in config/numAgents/test25* config/numAgents/test100* ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 100
#done

while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 1 ]; then
    # starte zweite Ladung
    for i in config/runStatic/2/test100*; do 
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
    for i in config/runPower/1/test100*; do 
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
    for i in config/runPower/2/test100*; do 
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
    for i in config/runStatic/1/test100*; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 100
done
    break
  fi
  sleep 600
done




#test agent number
#for i in config/pretest3/test1.ini config/pretest3/test2.ini config/pretest3/test3.ini config/pretest3/test4.ini config/pretest2/test5.ini config/pretest3/test6.ini config/pretest3/test7.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 1
#done



########### first batch ###############
#for i in config/pretest/test1.ini config/pretest/test2.ini config/pretest/test3.ini config/pretest/test4.ini config/pretest/test5.ini config/pretest/test6.ini config/pretest/test7.ini config/pretest/test8.ini config/pretest/test9.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 1
#done

############second batch ###############

#for i in config/pretest2/test10.ini config/pretest2/test11.ini config/pretest2/test12.ini config/pretest2/test13.ini config/pretest2/test14.ini config/pretest2/test15.ini config/pretest2/test16.ini config/pretest2/test17.ini config/pretest2/test18.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 1
#done

#for i in config/pretest/test10.ini config/pretest/test11.ini config/pretest/test12.ini config/pretest/test13.ini config/pretest/test14.ini config/pretest/test15.ini config/pretest/test16.ini config/pretest/test17.ini config/pretest/test18.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 1
#done

#offender/run.py blubb.ini | at now + 7 hours

#while true; do
#  NUMPROCS=`ps -ef| grep run.py | wc -l`
#  if [ $NUMPROCS -le 1 ]; then
#    # starte zweite Ladung
#    for i in config/testSequential/* ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 1
#done
#    break
#  fi
#  sleep 100
#done



 # ./multirun.sh |at now + 7 hours
  