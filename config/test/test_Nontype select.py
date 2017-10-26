import numpy as np
import math
import sys, psycopg2, os, time, random, logging
from operator import itemgetter
from collections import Counter


def popularVenue():
    mycurs = conn.cursor()
    mycurs.execute("""SELECT road_id, weighted_checkins FROM(
            SELECT venue_id, checkins_count,(checkins_count * 100.0)/temp.total_checkins as weighted_checkins
            from (SELECT COUNT(venue_id)as total_venues, SUM(checkins_count) as total_checkins FROM open.nyc_fs_venue_join
            ) as temp, open.nyc_fs_venue_join
            )
            AS fs LEFT JOIN open.nyc_road2fs_near r2f on r2f.fs_id=fs.venue_id WHERE NOT road_id is null""")
    roads=mycurs.fetchall() #returns tuple of tuples, venue_id,weighted_checkins
    #self.log.debug('popular Venue') 
    print(roads[0])
    return roads



def weightedChoice(roads, road):
    #TODO bring weihts to same scale!!!
    if not roads:
        roadId=None   
    elif (len(roads[0]) is 1):
        road=random.choice(roads)
        roadId=road[0]
    else:
        roadsList=[x[0] for x in roads]
        weightList=[x[1] for x in roads]
        if (len(roads[0])>2): #×or if self.targetType=2
            weightList2=[x[2] for x in roads]
            #bring both weights to same scala
            weightList2=[float(i*100) for i in weightList2]
            weightList=[i*j for i,j in zip(weightList,weightList2)]
            #self.log.debug('combined weights: {}'.format(weightList[0]))
        pWeightList=[]
        sumWeightList=sum(weightList)
        for value in weightList:
            pWeightList.append(value/sumWeightList)
        #self.log.debug('weightlist p sum: {}'.format(sum(pWeightList)))
        roadIdNp=np.random.choice(roadsList, 1, True, pWeightList)
        roadId=roadIdNp[0]  
    return roadId


def connectDB():
    try:
        conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
        mycurs=conn.cursor()
            #self.log.info("connected to DB")
    except Exception as e:
        sys.exit(1)
    return conn

conn=connectDB()
roads=popularVenue()
weightedChoice(roads, 100)
print(weightedChoice(roads, 100))