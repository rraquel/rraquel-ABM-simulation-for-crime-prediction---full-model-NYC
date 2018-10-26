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
mycurs.execute("""CREATE TABLE open.nyc_taxi_trips0706_1415_censuscoutns AS
SELECT censuspickup, censusdropoff, weight, c FROM (
(SELECT censuspickup, censusdropoff, SUM(weight) as weight, COUNT(*) as c FROM(
SELECT * FROM open.nyc_taxi_trips0106_new_censuscoutns
UNION ALL
SELECT * FROM open.nyc_taxi_trips0712_censuscoutns) as f1
GROUP BY censuspickup, censusdropoff
HAVING COUNT(*) > 1 Order by censuspickup, censusdropoff)
UNION ALL (
SELECT censuspickup, censusdropoff, SUM(weight) as weight, COUNT(*) as c FROM(
SELECT * FROM open.nyc_taxi_trips0106_new_censuscoutns
UNION ALL
SELECT * FROM open.nyc_taxi_trips0712_censuscoutns) as f2
GROUP BY censuspickup, censusdropoff
HAVING COUNT(*) = 1 Order by censuspickup, censusdropoff)) as g""")
#fetch all values into tuple
print("CREATE TABLE open.nyc_taxi_trips0706_1415_censuscoutns done")

conn.commit()
mycurs.execute("""select * from open.nyc_taxi_trips0706_1415_censuscoutns""")
result=mycurs.fetchall()
print(result[0])

