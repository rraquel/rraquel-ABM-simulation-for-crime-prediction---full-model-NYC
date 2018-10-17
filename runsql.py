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
mycurs.execute("""CREATE TABLE open.nyc_taxi_trips_new_censuspickup
    AS (select r.trip_id, r.pickup_ftus, r.passenger_count, ct.gid
    FROM open.nyc_taxi_trips_new as r, open_shapes.nyc_census_tract_e ct
    WHERE ST_DWithin(r.pickup_ftus, ct.geom_ftus, 5))""")
#fetch all values into tuple
print("CREATE TABLE open.nyc_taxi_trips_new_censuspickup done")

mycurs.execute("""CREATE TABLE open.nyc_taxi_trips_new_censusdropoff
    AS (select r.trip_id, r.dropoff_ftus, r.passenger_count, ct.gid
    FROM open.nyc_taxi_trips_new as r, open_shapes.nyc_census_tract_e ct
    WHERE ST_DWithin(r.dropoff_ftus, ct.geom_ftus, 50))""")
print("CREATE TABLE open.nyc_taxi_trips_new_censusdropoff done")

mycurs.execute("""CREATE TABLE open.nyc_taxi_trips_new_censuscoutns as (
    SELECT p.gid as censuspickup, d.gid as censusdropoff, count(*) as weight
    FROM open.nyc_taxi_trips_new as t
    RIGHT JOIN open.nyc_taxi_trips_new_censuspickup as p ON t.trip_id=p.trip_id
    RIGHT JOIN open.nyc_taxi_trips_new_censusdropoff as d ON t.trip_id=d.trip_id
    where t.trip_id is not null group by censuspickup, censusdropoff)""")
print("CREATE TABLE open.nyc_taxi_trips_new_censuscoutns done")

mycurs.execute("""SELECT count(distinct(censuspickup)) FROM open.nyc_taxi_trips_new_censuscoutns""")
result=mycurs.fetchall()
print(result)