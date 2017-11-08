while true; do
  NUMPROCS=`ps -ef| grep run.py | wc -l`
  if [ $NUMPROCS -le 3 ]; then
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
    for i in config/test/125/test125PPVC.ini config/test/125/test125PRV.ini; do 
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
    for i in config/test/125/test125PRVC; do 
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 10
done
    break
  fi
  sleep 600
done