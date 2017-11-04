import numpy as np
import math
from operator import itemgetter
from collections import Counter
import mesa
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import networkx as nx
import statistics
import psycopg2, sys, os, time, random, logging
from collections import Counter
from itertools import chain


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

def createRoadNetwork():
        # SQL to select data
        # from intersection2road table as i2r: intersection_id [key]
        # from open.nyc_road_proj_final as r: gid [1]
        # from open.nyc_road_attributes as ra: length [2], crimes_2015 [3]
        # join tables using road_id into gid
        
        roadLength=0
        #crimes_2015: n crime to 1 road mapping
        
        mycurs.execute("""select intersection_id,r.gid,length,crimes_2015 from 
            open.nyc_intersection2road i2r
            left join open.nyc_road_proj_final r on i2r.road_id = r. gid
            left join open.nyc_road_attributes ra on ra.road_id=r.gid""")
        #fetch all values into tuple
        interRoad=mycurs.fetchall()
        #dictionary {} -  a Key and a value, in this case a key and a set() of values -unordered collection
        intersect={}
        G=nx.Graph()
        #for each line in interRoad 
        for line in interRoad:
            #if attribute[0] (intersection_id) is not in intersect
            if not line[0] in intersect:
                #initialize a set for the key (intersect_id)
                intersect[line[0]]=set()
            #add current road_id to key
            intersect[line[0]].add(line[1])
            
            #add road, length and crimes as node info in graph
            #self.G.add_node(line[1], length=line[2], num_crimes=line[3])
            # TODO Parameter: Assumptions Humans walk 300 feet in 60s
            G.add_node(line[1],length=line[2])
        #for r in self.G.nodes_iter():
            #roadLength+=self.G.node[r]['length']
        #self.log.debug("Found {} intersections".format(len(intersect)))
        #self.log.debug("roadlenght: {}".format(roadLength))
        #build edges with information on nodes (roads)
        # loops over each intersection in intersect[]     
        for interKey in intersect.keys():
            #loops over each road in the current intersection
            for road in intersect[interKey]:
                #loops over roads again to compare roads and map relationship
                for road2 in intersect[interKey]:
                    if not road==road2:
                        G.add_edge(road, road2)
        return G

conn=connectDB()
G=createRoadNetwork
#roads=popularVenue()
#weightedChoice(roads, 100)
#print(weightedChoice(roads, 100))

road=68473
targetRoad=24863
try:
    way=nx.shortest_path(G,road,targetRoad,weight='length')
    print(way)
except Exception as e:
    print(e)