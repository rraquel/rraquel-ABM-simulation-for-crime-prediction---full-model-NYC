#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psycopg2, sys, os, time
from shapely.geometry import LineString
from shapely import wkb

debug = 0
t = time.process_time()
minRoad = 0

ipoints = {}
i2r = []


def connectDB(): 
  try:
    conn = psycopg2.connect("dbname='shared' user='ssandow' host='localhost' password='gvc4XVlIU8'")
  except Exception as e:
    print("I am unable to connect to the database"+str(e))
    sys.exit(1)
  return conn

def createIntersections(r):
    # Begin and End points
    global myIntersectId
    for point in [str(r[1]),str(r[2])]:
        success=0
        if point in ipoints.keys():
            intersect_id = ipoints[point]
            i2r.append([intersect_id,r[0]])
            successCount['entityRelation']+=1
        else:
            successCount['intersect']+=1
            successCount['entityRelation']+=1
            ipoints[point] = myIntersectId
            i2r.append([myIntersectId,r[0]])
            myIntersectId += 1
            
    
def getAllRoads():
    myIntersectId = 1
    roadCurs = conn.cursor()
    sql = "select gid,ST_Startpoint(geom),ST_Endpoint(geom) from open.nyc_road_proj_final"
    roadCurs.execute(sql)
    res = [1]
    
    while (len(res) >=1):
        res = roadCurs.fetchmany(1000)
        #print("Time: {0}, RoadId: {1},".format(time.process_time() -t,res[0][0]))
        if len(res)>0:
            if (res[0][0] >= minRoad):
                for r in res:
                    successCount['road'] += 1
                    createIntersections(r)
        if debug:
            print('Debug is active. Ending now.')
            res=[]

        print("Success counters: {0}".format(str(successCount)))
    for l in i2r:
        filei2r.write("{},{}\n".format(l[0],l[1]))
    for i in ipoints.keys():
        fileintersect.write("{},{}\n".format(i,ipoints[i]))

filei2r = open('i2r_3.sql','w')
fileintersect = open('intersect_3.sql','w')
myIntersectId = 1
successCount = {'road':0,'intersect':0,'entityRelation':0}
conn = connectDB()
getAllRoads()
