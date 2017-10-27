#!/bin/bash

for i in config/pretestMu/* ; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done



#for i in config/pretestMU/test1.ini config/pretestMU/test2.ini config/pretestMU/test3.ini config/pretestMU/test4.ini config/pretestMU/test5.ini config/pretestMU/test6.ini config/pretestMU/test7.ini config/pretestMU/test8.ini config/pretestMU/test9.ini config/pretestMU/test10.ini ; do 
#    offender/run.py `echo "$i"|sed -e 's:config/::'` &
#    sleep 1
#done