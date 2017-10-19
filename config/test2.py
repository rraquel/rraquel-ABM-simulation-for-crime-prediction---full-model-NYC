import random
import sys, psycopg2, os, time, random, logging
import networkx as nx
from random import choices
import pandas as pd
import numpy as np
import pylab as pl
from collections import Counter
from datetime import datetime




def connectDB():
        try:
            conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
            curs=conn.cursor()
            logging.info("connected to DB")
        except Exception as e:
            logging.debug("not connected")
        return conn


conn=connectDB()
curs = conn.cursor()

road=10
time=datetime.now().time()
print('start at: {}'.format(time))
crimes2=[]

curs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft WHERE road_id ={}"""
    .format(road))
crimes=curs.fetchall()
for crime in crimes:
    crimes2.append(crime[0])

curs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_BURGLARY WHERE road_id ={}"""
            .format(road))
crimes=curs.fetchall()
for crime in crimes:
    crimes2.append(crime[0])

curs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_ROBBERY WHERE road_id ={}"""
            .format(road))
crimes=curs.fetchall()
for crime in crimes:
    crimes2.append(crime[0])

curs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_LARCENY WHERE road_id ={}"""
            .format(road))
crimes=curs.fetchall()
for crime in crimes:
    crimes2.append(crime[0])

curs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_ASSAULT WHERE road_id ={}"""
            .format(road))
crimes=curs.fetchall()
for crime in crimes:
    crimes2.append(crime[0])

curs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_LARCENY_MOTOR WHERE road_id ={}"""
            .format(road))
crimes=curs.fetchall()
for crime in crimes:
    crimes2.append(crime[0])

curs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_RAPE WHERE road_id ={}"""
            .format(road))
crimes=curs.fetchall()
for crime in crimes:
    crimes2.append(crime[0])

time=datetime.now().time()
print('end at: {}'.format(time))


time=datetime.now().time()
print('start at: {}'.format(time))
curs.execute("""SELECT object_id, crimetype from open.nyc_road2police_incident_5ft_types WHERE road_id ={}"""
    .format(road))
crimes=curs.fetchall()
for crime in crimes:
    if crime[1] is 0:
        crimes2.append(crime[0])
    elif crime[1] is 1:
        crimes2.append(crime[0])
    elif crime[1] is 2:
        crimes2.append(crime[0])
    elif crime[1] is 3:
        crimes2.append(crime[0])
    elif crime[1] is 4:
        crimes2.append(crime[0])
    elif crime[1] is 5:
        crimes2.append(crime[0])
    elif crime[1] is 6:
        crimes2.append(crime[0])
time=datetime.now().time()
print('end at: {}'.format(time))

