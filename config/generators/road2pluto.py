#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Find foursquare venues in max 80 feet distance for each road
#

import psycopg2, sys, os, time
from shapely.geometry import LineString
from shapely import wkb



dir_path = os.path.dirname(os.path.realpath(__file__))

debug=1
t = time.monotonic()
minRoad=0

def connectDB(): 
  try:
    conn = psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b'")
  except Exception as e:
    print("I am unable to connect to the database"+str(e))
    sys.exit(1)
  return conn

def getNearbyElement(road):
    curs = conn.cursor()
    # Hard coded 80 feet distance
    sql="select gid from open.nyc_pluto_areas where st_dwithin(st_geomfromtext('{}',2263),geom,80)".format(road[1])
    curs.execute(sql)
    res=curs.fetchall()
    for line in res:
        filesql.write("{},{}\n".format(road[0],line[0]))
    
def getAllRoads():
    roadCurs = conn.cursor()
    sql="select gid,st_astext(geom) from open.nyc_road_proj_final"
    roadCurs.execute(sql)
    res=[1]
    
    while (len(res) >=1):
        res = roadCurs.fetchmany(1000)
        #print("Time: {0}, RoadId: {1},".format(time.process_time() -t,res[0][0]))
        if len(res)>0:
            print("Got another 1k. Running for {}s already.".format(time.monotonic()-t))
            for road in res:
                getNearbyElement(road)    

filesql=open(os.path.join(dir_path,'..','data','sql','road2pluto2.sql'),'w')
conn = connectDB()
getAllRoads()
