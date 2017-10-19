for i in config/perftest/*.ini; do
    offender/run.py `echo "$i"|sed -e 's:config/::'` &
    sleep 1
done
