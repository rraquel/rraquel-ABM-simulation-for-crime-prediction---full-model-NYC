#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psycopg2, sys, os, time, random, logging

conn= psycopg2.connect("dbname='shared' user='rraquel' host='127.0.0.1' password='Mobil4b' ")
mycurs=conn.cursor()
print("start query")
mycurs.execute("""UPDATE open.nyc_taxi_trips_new SET trip_month_pickup=(extract(month from dropoff_datetime::timestamp))""")
#fetch all values into tuple
print("update done")
mycurs.execute("""select count(*) from open.nyc_taxi_trips where trip_month_pickup is null""")
print("count done")
result=mycurs.fetchall()
print(result)