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
    conn = psycopg2.connect("dbname='shared' user='ssandow' host='localhost' password='gvc4XVlIU8'")
  except Exception as e:
    print("I am unable to connect to the database"+str(e))
    sys.exit(1)
  return conn


# TODO Use fs_venue_joined instead of ..._location
def getNearbyRoad(venue):
    curs = conn.cursor()
    # Hard coded 80 feet distance
    sql="""select gid from open.nyc_road_proj_final where st_dwithin(st_geomfromtext('{}',2263),geom,80) order by 
      st_distance(st_geomfromtext('{}',2263),geom) asc limit 1""".format(venue[1], venue[1])
    try:
        curs.execute(sql)
        res=curs.fetchall()
    except Exception as e:
        print("SQL failed", sql, e)
        res=[]
        conn.rollback()
    for line in res:
        filesql.write("{},{}\n".format(venue[0],line[0]))
    
def getAllVenues():
    # Use only venues in any of the 5 boroughs
    # bCurs= conn.cursor()
    # sql = """select gid from open.nyc_boroughs"""
    # boroughs = bCurs.fetchall()
    # for borough in boroughs:    
      venueCurs = conn.cursor()
      sql = """select location_id, st_astext(ftus_coord) from open.nyc_fs_venue_location"""
      #sql="select gid,st_astext(geom) from open.nyc_road_proj_final"
      venueCurs.execute(sql)
      res=[1]
      
      while (len(res) >=1):
          res = venueCurs.fetchmany(1000)
          #print("Time: {0}, RoadId: {1},".format(time.process_time() -t,res[0][0]))
          if len(res)>0:
              print("Got another 1k. Running for {}s already.".format(time.monotonic()-t))
              for venue in res:
                  getNearbyRoad(venue)    

filesql=open(os.path.join(dir_path,'..','data','sql','road2fs_nearest.sql'),'w')
conn = connectDB()
getAllVenues()
