#!/bin/bash

#list=[]
#to run: in pythonprototype folder: bash offender/multirun.sh


#test agent number
#for i in config/pretest3/test1.ini config/pretest3/test2.ini config/pretest3/test3.ini config/pretest3/test4.ini config/pretest2/test5.ini config/pretest3/test6.ini config/pretest3/test7.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 1
#done



########### first batch #################
#for i in config/pretest2/test1.ini config/pretest2/test2.ini config/pretest2/test3.ini config/pretest2/test4.ini config/pretest2/test5.ini config/pretest2/test6.ini config/pretest2/test7.ini config/pretest2/test8.ini config/pretest2/test9.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 1
#done

for i in config/numAgents/1/test200* ; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done


#for i in config/pretest/test10.ini config/pretest/test11.ini ; do 
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
#  if [$NUMPROCS -le 1]; then
#    # starte zweite Ladung
#    for i in config/pretest/test10.ini config/pretest/test11.ini config/pretest/test12.ini config/pretest/test13.ini config/pretest/test14.ini config/pretest/test15.ini config/pretest/test16.ini config/pretest/test17.ini config/pretest/test18.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 1
#done
#    break
#  fi
#  sleep 10
#done



 # ./multirun.sh |at now + 7 hours
  