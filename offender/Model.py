#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mesa
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
        self.log.info('Number of Agents: {}'.format(self.numAgents))
        self.agentTravelAvg = modelCfg.getfloat('agentTravelAvg')

        #defubes target selection tpye
        self.targetType= modelCfg.getint('targetType')
        if self.targetType>2:
           self.log.critical("Target type in ini-file is out of range: {}".format(self.targetType))
           raise SystemExit(1)
        #defines the starting location type 
        self.startLocationType= modelCfg.getint('startLocationType')
        if self.startLocationType>1:
            self.log.critical("Starting location type is out of range {}".format(self.startLocationType))
        
        self.centerAttract=modelCfg.getint('centerAttract')
        if self.startLocationType>1:
            self.log.critical("Center attractiveness aout of range {}".format(self.centerAttract))


        #parameters for radius search
        self.staticRadius=modelCfg.getint('staticRadius')
        self.uniformRadius=self.staticRadius*2
        self.mu=0.6
        self.dmin=2.5
        self.dmax=530
       
        #no switch case in python - can use dictionary and switch function
        self.radiusType=modelCfg.getint('radiusType')
        if self.radiusType>2:
            self.log.critical("Radius type in ini-file is out of range: {}".format(self.radiusType))
            raise SystemExit(1)
                    
        #self.agentStartLocationFinder=modelCfg.get('agentStartLocationFinder', findStartLocationRandom)
        self.schedule=RandomActivation(self)
        
        self.totalCrimes=0

        self.log.info("Generating Model")

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
            #"passedCrimesUnique": lambda a: a.crimesUnique,
            "searchRadius": lambda a: a.searchRadius
            })
        
        #create roadNW
        self.G=self.createRoadNetwork()
        
        #create agent
        #TODO give agent the number of steps one should move - distribution ~1-7
        #TODO include start location type (to tune starting point with PLUTO info) and demographics
        for i in range(self.numAgents):
            try:
                a=AgentX(i, self, self.radiusType, self.targetType, self.startLocationType, self.agentTravelAvg, self.centerAttract)
                self.schedule.add(a)
                self.log.info("Offender created")
            except:
                self.log.critical("Agents could not be created")
                raise SystemExit(1)
        self.log.info("{} agents created".format(self.numAgents))

    def connectDB(self):
        try:
            self.conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
            self.curs=self.conn.cursor()
            self.log.info("connected to DB")
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
            self.G.node[line[1]]['crimesList'].add(line[3])
        #for r in self.G.nodes_iter():
            #roadLength+=self.G.node[r]['length']
        self.log.debug("Found {} intersections".format(len(intersect)))
        self.log.debug("roadlenght: {}".format(roadLength))
        #build edges with information on nodes (roads)
        # loops over each intersection in intersect[]     
        for interKey in intersect.keys():
            #loops over each road in the current intersection
            for road in intersect[interKey]:
                #loops over roads again to compare roads and map relationship
                for road2 in intersect[interKey]:
                    if not road==road2:
                        self.G.add_edge(road, road2)
        self.log.debug("Number of  G: roads: {0}, intersections: {1}".format(self.G.number_of_nodes(), self.G.number_of_edges))
        self.log.debug("Isolated roads: {0}".format(len(nx.isolates(self.G))))
        self.log.info("roadNW built, intersection size: {0}".format(len(intersect)))
        self.log.info("roadNW built, roads size: {0}".format(self.G.number_of_nodes()))
        return self.G

    def step(self, i, numSteps):
        """advance model by one step."""
        self.modelStepCount=i
        self.generalNumSteps=numSteps
        #print('==> model step count {}'.format(self.modelStepCount))
        self.dc.collect(self)
        self.schedule.step()