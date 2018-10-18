#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psycopg2, sys, os, time, random, logging
from time import sleep

conn= psycopg2.connect("dbname='shared' user='rraquel' host='127.0.0.1' password='Mobil4b' ")
mycurs=conn.cursor()

#◙count=99
#i=0
#while not count==0:
#    print("sleep")
#    sleep(18000)
#    print("try count")
#    mycurs.execute("""select count(*) from open.nyc_taxi_trips_new where trip_month_pickup is null;""")
#    count=mycurs.fetchall()[0][0]
#    i=i+1
#    print(i)
#    print(count)
#    if i>20:
#        print("exit")
#        exit()

print("start query")
mycurs.execute("""CREATE TABLE open.aaaaaaaaTest
  AS (select * FROM open.nyc_taxi_trips limit 10""")
#fetch all values into tuple
print("CREATE TABLE open.nyc_taxi_trips0712_censuspickup done")


mycurs.execute("""select * from open.aaaaaaaaTest""")
result=mycurs.fetchall()
print(result)

conn.commit()