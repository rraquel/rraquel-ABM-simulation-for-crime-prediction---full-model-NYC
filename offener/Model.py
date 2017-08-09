import mesa
from Agent import Agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import networkx as nx
import numpy as np
import math
import psycopg2, sys, os, time, random, logging

class Model(mesa.Model):
    """ characteristics of the model."""
    def __init__(self, modelCfg):
        self.log=logging.getLogger('')
        
        # Get Model parameters from config. Set small default values so errors pop up
        self.numAgents=modelCfg.getint('numAgents')
        self.agentReTravelAvg = modelCfg.getfloat('agentReTravelAvg',1.1)

        #parameters for radius search
        self.mu=modelCfg.getfloat('mu')
        self.dmin=modelCfg.getfloat('dmin')
        self.dmax=modelCfg.getint('dmax')
        self.staticRadius=modelCfg.getint('staticRadius')
        
        #self.agentStartLocationFinder=modelCfg.get('agentStartLocationFinder', findStartLocationRandom)
        self.schedule=RandomActivation(self)
        
        self.totalCrimes=0

        self.connectDB()
        self.log.info('Generating Model')

        #TODO data collection
        #collect statistics from peragent&step (can be more)
        self.dc=DataCollector(model_reporters={} , agent_reporters={})

        #create roadNW
        self.createRoadNetwork()
        
        #select startingPoint
        starts=random.sample(self.G.nodes(),self.numAgents+1)

        #create agent
        for i in range(self.numAgents):
            a=Agent(i, self, starts[i], self.findTargetLocation(starts[i]))
            self.schedule.add(a)
            self.log.info("Offender created")
        print("agents created")

    def connectDB(self):
        try:
            self.conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
            self.curs=self.conn.cursor()
        except Exception as e:
            self.log.error("connection to DB failed"+str(e))
            sys.exit(1)
    
    def createRoadNetwork(self):
        # SQL to select data
        # from intersection2road table as i2r: intersection_id [key]
        # from open.nyc_road_proj_final as r: gid [1]
        # from open.nyc_road_attributes as ra: length [2], crimes_2015 [3]
        # join tables using road_id into gid
        
        #crimes_2015: n crime to 1 road mapping
        
        self.curs.execute("""select intersection_id,r.gid,length,crimes_2015 from 
            open.nyc_intersection2road i2r
            left join open.nyc_road_proj_final r on i2r.road_id = r. gid
            left join open.nyc_road_attributes ra on ra.road_id=r.gid""")
        #fetch all values into tuple
        interRoad=self.curs.fetchall()
        #dictionary {} -  a Key and a value, in this case a key and a set() of values -unordered collection
        intersect={}
        self.G=nx.Graph()
        #for each line in interRoad 
        for line in interRoad:
            #if attribute[0] (intersection_id) is not in intersect
            if not line[0] in intersect:
                #initialize a set for the key (intersect_id)
                intersect[line[0]]=set()
            #add current road_id to key
            intersect[line[0]].add(line[1])
            self.totalCrimes+=line[3]
            #add road, length and crimes as node info in graph
            self.G.add_node(line[1], length=line[2], num_crimes=line[3])
        self.log.debug("Found {} intersections".format(len(intersect)))
        #build edges with information on nodes (roads)
        # loops over each intersection in intersect[]     
        for interKey in intersect.keys():
            #loops over each road in the current intersection
            for road in intersect[interKey]:
                #loops over roads again to compare roads and map relationship
                for road2 in intersect[interKey]:
                    if not road==road2:
                        self.G.add_edge(road, road2)
        self.log.debug("Length of  G: roads: {0}, intersections: {1}".format(self.G.number_of_nodes(), self.G.number_of_edges))
        self.log.debug("Isolated roads: {0}".format(len(nx.isolates(self.G))))
        print('roadNW built, intersection size: {0}'.format(len(intersect)))
        print('roadNW built, roads size: {0}'.format(self.G.number_of_nodes()))

    def findTargetLocation(self,road):
        mycurs = self.conn.cursor()
        targetRoad=0

        #TODO imput radius selection options - distance
        searchRadius=40000 #fixed search radius for target
        roadDistance=400 
        maxRadius=searchRadius*1.025
        minRadius=searchRadius*0.925

        while targetRoad==0:
            mycurs.execute("""select road_gid,t_dist from (
                select road.gid as road_gid,ST_Distance(ST_Centroid(road.geom), ftus_coord) as t_dist from open.nyc_road_proj_final as road, ( 
                select location_id,distance,ftus_coord from (
                    select location_id,ST_distance(ftus_coord,(
                        select ST_centroid(geom) from open.nyc_road_proj_final where gid={0})) as distance, ftus_coord from open.nyc_fs_venue_location) as foo 
                where distance between {1} and {2} limit 2) as rd_table ) as bar 
                where t_dist < {3} order by t_dist asc limit 1""".format(road,minRadius,maxRadius,searchRadius))
            roadId=mycurs.fetchone() #returns tuple with first row (unordered list)
            if not roadId is None:
                targetRoad=roadId[0]
                print("roadid in target: {0}".format(roadId[0]))
                return (targetRoad)
            searchRadius=searchRadius/10

    def powerRadius(self, mu, dmin, dmax):
        beta=1+mu
        pmax = math.pow(dmin, -beta)
        pmin = math.pow(dmax, -beta)
        uniformProb=np.random.uniform(pmin, pmax)
        #levy flight: P(x) = Math.pow(x, -1.59) - find out x? given random probability within range
        powerKm =  (1/uniformProb)*math.exp(1/beta)
	    #levy flight gives distance in km - transform km to foot
        powerRadius = powerKm * 3280.84
        print ("power search radius: {0}".format(powerRadius))
        return powerRadius


    def step(self):
        """advance model by one step."""
        self.dc.collect(self)
        self.schedule.step()