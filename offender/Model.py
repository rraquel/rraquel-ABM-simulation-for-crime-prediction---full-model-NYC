#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mesa
from Agent import Agent
from AgentX import AgentX
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import networkx as nx
import numpy as np
import math
import psycopg2, sys, os, time, random, logging

class Model(mesa.Model):
    """ characteristics of the model."""
    def __init__(self, modelCfg):
        #for batch runner: instance attribute running in Model class - enables conditional shut off of the model once a condition is met.
        self.running = True

        self.log=logging.getLogger('')
        self.conn=self.connectDB()
        self.generalNumSteps=0

        self.generalSteps=modelCfg.getint('numAgents')
        
        # Get Model parameters from config. Set small default values so errors pop up
        self.numAgents=modelCfg.getint('numAgents')
        self.agentTravelAvg = modelCfg.getfloat('agentTravelAvg')

        #defubes target selection tpye
        self.targetType= modelCfg.getint('targetType')
        #defines the starting location type 
        self.startLocationType= modelCfg.getint('startLocationType')

        #parameters for radius search
        self.staticRadius=modelCfg.getint('staticRadius')
        print("static radius: {0}".format(self.staticRadius))
        self.uniformRadius=self.staticRadius*2
        print("uniform radius: {0}".format(self.uniformRadius))
        self.mu=modelCfg.getfloat('mu')
        self.dmin=modelCfg.getfloat('dmin')
        self.dmax=modelCfg.getint('dmax')
       
        #no switch case in python - can use dictionary and switch function
        self.radiusType=modelCfg.getint('radiusType')
        #print("radius type switch test: {0}".format(self.radiusType2))
        
        #self.agentStartLocationFinder=modelCfg.get('agentStartLocationFinder', findStartLocationRandom)
        self.schedule=RandomActivation(self)
        
        self.totalCrimes=0

        
        self.log.info('Generating Model')

        #TODO data collection
        #collect statistics from peragent&step (can be more) - see output in model
        self.dc=DataCollector(model_reporters={
            #"modelStepCount": lambda m: m.modelStepCount,
            "agentCount":lambda m: m.schedule.get_agent_count(),
            "radiusType": lambda m: m.radiusType,
            "targetType": lambda m: m.targetType,
            "totalCrimes": lambda m: m.totalCrimes, 
            #is this the average seen crimes over all the agents?
            "totalpassedCrimes": lambda m: sum(map(lambda a: a.seenCrimes,m.schedule.agents)),
            "totaltraveledDistance": lambda m: sum(map(lambda a: a.walkedDistance,m.schedule.agents)),
            "traveledRoads": lambda m: sum(map(lambda a: a.walkedRoads,m.schedule.agents)),
            "avgSearchRadius": lambda m: sum(map(lambda a: a.searchRadius,m.schedule.agents)),
            #"pai": lambda m: (((sum(map(lambda a: (a.seenCrimes+1),m.schedule.agents)))/m.totalCrimes)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/40986771),
            "pai2": lambda m: (((sum(map(lambda a: (a.seenCrimes+1),m.schedule.agents)))/m.totalCrimes)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/40986771) if m.modelStepCount is (m.generalNumSteps-1) else 0
            #"SD_distance": lambda m: (sqrt(lambda a: a.walkedDistance - (sum(map(a.walkedDistance,m.schedule.agents))/self.numAgents)))
            } ,
        agent_reporters={
            "startRoad": lambda a: a.startRoad,
            "passedCrimes": lambda a: a.seenCrimes,
            "traveledDistance": lambda a: a.walkedDistance,
            "passedCrimesUnique": lambda a: a.crimesUnique,
            "searchRadius": lambda a: a.searchRadius
            })
        
        #create roadNW
        self.G=self.createRoadNetwork()
        
        #create agent
        #TODO give agent the number of steps one should move - distribution ~1-7
        #TODO include start location type (to tune starting point with PLUTO info) and demographics
        for i in range(self.numAgents):
            if 0<= self.targetType <=2:
                a=AgentX(i, self, self.radiusType, self.targetType, self.startLocationType, self.agentTravelAvg)
            else:
                sample=random.sample(self.G.nodes(),self.numAgents+1)
                starts=sample[0]
                print('print road{0}'.format(starts))
                a=Agent(i, self, starts, self.radiusType)
            self.schedule.add(a)
            self.log.info("Offender created")
        print("agents created")

    def connectDB(self):
        try:
            self.conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
            self.curs=self.conn.cursor()
            print("connected to DB")
        except Exception as e:
            self.log.error("connection to DB failed"+str(e))
            sys.exit(1)
        return self.conn
    
    def createRoadNetwork(self):
        # SQL to select data
        # from intersection2road table as i2r: intersection_id [key]
        # from open.nyc_road_proj_final as r: gid [1]
        # from open.nyc_road_attributes as ra: length [2], crimes_2015 [3]
        # join tables using road_id into gid
        
        roadLength=0
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
            #self.G.add_node(line[1], length=line[2], num_crimes=line[3])
            # TODO Parameter: Assumptions Humans walk 300 feet in 60s
            self.G.add_node(line[1],length=line[2],num_crimes=line[3],crimesList=set())
            #self.G.node[line[1]]['crimesList'].add(line[3])
            roadLength+=line[2]
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
        print('road lenght total: {}'.format(roadLength))
        print('road lenght total: {}'.format(type(roadLength)))
        return self.G

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
                #print("roadid in target: {0}".format(roadId[0]))
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


    def step(self, i, numSteps):
        """advance model by one step."""
        self.modelStepCount=i
        self.generalNumSteps=numSteps
        #print('==> model step count {}'.format(self.modelStepCount))
        self.dc.collect(self)
        self.schedule.step()