#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mesa
from AgentX import AgentX
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import networkx as nx
import numpy as np
import math
import statistics
import psycopg2, sys, os, time, random, logging
from collections import Counter
from itertools import chain
import globalVar
import QRunner

class Model(mesa.Model):
    """ characteristics of the model."""
    def __init__(self, modelCfg):
        #for batch runner: instance attribute running in Model class - enables conditional shut off of the model once a condition is met.
        self.t=time.monotonic()
        #self.insertQ = QRunner.QRunner()
        self.running = True
        self.run_id=0
        self.log=logging.getLogger('')
        self.log.info("Starting to build model")
        self.conn=self.connectDB()
        print("connected to db for model")
        self.generalNumSteps=0

        self.generalSteps=modelCfg.getint('numAgents')
        
        # Get Model parameters from config. Set small default values so errors pop up
        self.numAgents=modelCfg.getint('numAgents')
        self.log.info('Number of Agents: {}'.format(self.numAgents))
        self.agentTravelAvg = modelCfg.getfloat('agentTravelAvg')

        #defubes target selection tpye
        self.targetType= modelCfg.get('targetType')
        #defines the starting location type 
        self.startLocationType= modelCfg.get('startLocationType')

        #parameters for radius search
        self.staticRadius=modelCfg.getint('staticRadius')
        self.uniformRadius=self.staticRadius*2
        try:
            self.mu=modelCfg.getfloat('powermu')
        except Exception as e:
            self.log.info("no mu for power radius set, mu default 0.6")
        else:
            self.mu=0.6
            self.log.info("no mu for power radius set, mu default 0.6")
        self.dmin=2.5
        self.dmax=530
       
        #no switch case in python - can use dictionary and switch function
        self.distanceType=modelCfg.get('distanceType')

        #wayfindingType
        self.wayfindingType=modelCfg.get('wayfindingType')

        #self.agentStartLocationFinder=modelCfg.get('agentStartLocationFinder', findStartLocationRandom)
        self.schedule=RandomActivation(self)

        #build crimes
        self.allCrimes={}
        self.burglaryCount=1
        self.robberyCount=1
        self.larcenyCount=1
        self.larcenyMCount=1
        self.assualtCount=1
        self.totalCrimes=1
        self.createCrimes()
        self.log.info("time after createCrimes: {}".format(str(time.monotonic()-self.t)))
        if self.allCrimes is None:
            self.log.critical("no crimes loaded")

        #build residential area
        self.totalresidentialRoads=1
        self.residentRoads=[]
        self.residentRoadsWeight=[]
        self.createResidential()

        self.taxiTracts=dict()
        self.createTaxiTrips()

        self.crimeCT=dict()
        self.createCrimeCT()

        self.totalRoadDistance=40986771

        self.log.info("Generating Model")

        #collect statistics from peragent&step (can be more) - see output in model
        #!!!!LOGS VARIABLES OF THE AGENT AT THE BEGINNING OF THE STEP!!!!!! THEREFORE NEED TO ADD 1 STEP TO THE RUN
        self.dc=DataCollector(model_reporters={} ,
        agent_reporters={
            #"current Road": lambda a: a.road,
            "traveledDistance": lambda a: a.walkedDistance,
            })
        
        #create roadNW
        self.roadLengthdict=dict
        self.G=nx.Graph()
        self.G2=nx.Graph()
        self.roads=dict()
        self.intersect=dict()
        self.createRoadNetwork()
        self.log.info("time after roadNW: {}".format(str(time.monotonic()-self.t)))
        
        #create agent
        #TODO give agent the number of steps one should move - distribution ~1-7
        #TODO include start location type (to tune starting point with PLUTO info) and demographics
        for i in range(self.numAgents):
            try:
                a=AgentX(i, self, self.distanceType, self.targetType, self.startLocationType, self.agentTravelAvg)
                self.schedule.add(a)
                #self.log.info("Offender created")
            except Exception as e:
                self.log.critical("Agents could not be created: " + str(e))
                raise SystemExit(1)
        self.log.info("{0} agents created, time {1}".format(self.numAgents,str(time.monotonic()-self.t)))

    def connectDB(self):
        try:
            print('here')
            #self.conn= psycopg2.connect("dbname='shared' port=5433 user='rraquel' host='127.0.0.1' password='Mobil4b' ")        
            self.conn= psycopg2.connect("dbname='shared' user='rraquel' host='127.0.0.1' password='Mobil4b' ")
            self.mycurs=self.conn.cursor()
            #self.log.info("connected to DB")
        except Exception as e:
            self.log.critical("connection to DB failed"+str(e))
            sys.exit(1)
        return self.conn
    
    def createRoadNetwork(self):
        # SQL to select data
        # from intersection2road table as i2r: intersection_id [key]
        # from open.nyc_road_proj_final as r: gid [1]
        # from open.nyc_road_attributes as ra: length [2], crimes_2015 [3]
        # join tables using road_id into gid
        
        roadLength=0
        weightdict=dict()
        #crimes_2015: n crime to 1 road mapping
        #open.nyc_road_attributes without and open.nyc_road_attributes2 with census tract for each road
        self.mycurs.execute("""select intersection_id,r.gid, length, ra.st_width, roadtypew, crimes_2015, censustract from 
            open.nyc_intersection2road i2r
            left join open.nyc_road_proj_final r on i2r.road_id = r. gid
            left join open.nyc_road_attributes2 ra on ra.road_id=r.gid""")
        #fetch all values into tuple
        interRoad=self.mycurs.fetchall()
        #dictionary {} -  a Key and a value, in this case a key and a set() of values -unordered collection
        
        #for each line in interRoad 
        for line in interRoad:
            #if attribute[0] (intersection_id) is not in intersect
            if not line[0] in self.intersect:
                #initialize a set for the key (intersect_id)
                self.intersect[line[0]]=set()
            #add current road_id to key
            self.intersect[line[0]].add(line[1])
        #for G2
        for line in interRoad:
            if not line[1] in self.roads:
                self.roads[line[1]]=set()
            self.roads[line[1]].add(line[0])            
            #add road, length and crimes as node info in graph
            #self.G.add_node(line[1], length=line[2], num_crimes=line[3])
            # TODO Parameter: Assumptions Humans walk 300 feet in 60s
            self.G.add_node(line[1],length=line[2], width=line[3], roadtype=line[4], census=line[6])
            self.G2.add_node(line[0])
            weightdict[line[1]]=[line[2], line[3], line[4], line[6]]
        #for r in self.G.nodes_iter():
            #roadLength+=self.G.node[r]['length']
        #self.log.debug("Found {} intersections".format(len(intersect)))
        #self.log.debug("roadlenght: {}".format(roadLength))
        #build edges with information on nodes (roads)
        # loops over each intersection in intersect[]     
        for interKey in self.intersect.keys():
            #loops over each road in the current intersection
            for road in self.intersect[interKey]:
                #loops over roads again to compare roads and map relationship
                for road2 in self.intersect[interKey]:
                    if not road==road2:
                        self.G.add_edge(road, road2)
        #for G2
        for roadKey in self.roads.keys():
            #loop over each intersection in roads
            for inters in self.roads[roadKey]:
                #loop over intersection again to compare intersect and map relationship
                for inters2 in self.roads[roadKey]:
                    if not inters==inters2:
                        self.G2.add_edge(inters, inters2, length=weightdict[roadKey][0], width=weightdict[roadKey][1], lengthwidth=(weightdict[roadKey][0]*weightdict[roadKey][1]), roadtype=weightdict[roadKey][2], roadtypelength=(weightdict[roadKey][0]*weightdict[roadKey][2]), census=weightdict[roadKey][3])

        self.log.debug("Number of  G: roads: {0}, intersections: {1}".format(self.G.number_of_nodes(), self.G.number_of_edges))
        self.log.debug("Number of  G2: roads: {1}, intersections: {0}".format(self.G2.number_of_nodes(), self.G2.number_of_edges))
        #self.log.debug("Isolated roads: {0}".format(len(nx.isolates(self.G))))
        #self.log.info("roadNW built, intersection size: {0}".format(len(intersect)))
        #self.log.info("roadNW built, roads size: {0}".format(self.G.number_of_nodes()))
        
        
        """      
        117320	total	100%
        115694	minus isolates	98.61%
        113182	minus detached	96.47%
        """
        self.mycurs.execute("""select * from open.nyc_road_proj_final_isolates""")
        #fetch all values into tuple
        globalVar.isolateRoadsRNW.update(self.mycurs.fetchall())

        #print(self.G.node[5134]['length'])
        #print(self.G.node[5134]['width'])
        #output is not a list of roads, but list of ('road_id')


    def createCrimes(self):
        #used until 13.12.2018 - also in for AAMAS submission
        #self.mycurs.execute("""SELECT * from open.nyc_road2police_incident_5ft_types_Jun WHERE NOT off_type is NULL""")
        self.mycurs.execute("""SELECT road_id, object_id, offense, off_type from open.nyc_road2pi_5ft_2015_jun""")
        #Burglary 1, robbery 2, grand Larceny 3, assualt 4, grand larceny motor 5
        rows=self.mycurs.fetchall()
        #print(rows[0])
        self.totalCrimes=len(rows)
        self.log.info("total number of crimes {}".format(self.totalCrimes))
        roadCrime={} 
        typeList=[]  
        typeCounter=Counter()
        #print(rows[0])
        crimeCount=0
        for line in rows:  
            crimes=[]            
            road=line[0]
            #print(road)
            crime=line[1]
            #print(crime)
            crimetype1=line[2]
            #print(crimetype1)
            crimetype=line[3]
            #print(crimetype)
            typeList.append(crimetype)
            #tuple with crime and crimetype
            tup=(crime,crimetype,crimetype1)
            crimes.append(tup)
            if roadCrime.get(road) is None:
                roadCrime[road]=crimes
            else:
                existingvalue=roadCrime[road]
                newvalue=existingvalue+crimes
                roadCrime[road]=newvalue
            #print(roadCrime)
        typeCounter=Counter(typeList)
        self.burglaryCount=typeCounter[1]
        self.robberyCount=typeCounter[2]
        self.larcenyCount=typeCounter[3]
        self.larcenyMCount=typeCounter[5]
        self.assualtCount=typeCounter[4]
        self.totalCrimes=sum(typeCounter.values())
        self.allCrimes=dict(roadCrime)
    
    def createResidential(self):
        self.mycurs.execute("""select distinct(r2p.road_id),census_population_weight
            from open.nyc_road2pluto_80ft r2p left join open.nyc_pluto_areas p 
            on r2p.road_id=p.gid where census_population_weight >0 AND 
            (landuse='01' OR landuse='02'  OR landuse='03' OR landuse='04')
            AND road_id not in (select gid from open.nyc_road_proj_final_isolates)""") 
        roads=self.mycurs.fetchall()
        self.totalresidentialRoads=len(roads)
        roadsList=[x[0] for x in roads]
        weightList=[x[1] for x in roads if x != None]
        pWeightList=[]
        sumWeightList=sum(weightList)
        for value in weightList:
            pWeightList.append(value/sumWeightList)
        self.residentRoads=roadsList
        self.residentRoadsWeight=pWeightList

    def createTaxiTrips(self):
        self.mycurs.execute("""SELECT censuspickup, censusdropoff, weight FROM
        open.nyc_taxi_trips0706_1415_censuscoutns""")
        #TODO fix open.nyc_taxi_trips_new_june2015_censuscoutns_weight; pweight
        census=self.mycurs.fetchall()
        
        for line in census:
            dropoff=dict()                        
            dropoff[line[1]]=line[2]
            if line[0] in self.taxiTracts:
                temp=self.taxiTracts[line[0]]
                temp[line[1]]=line[2]
                self.taxiTracts[line[0]]=temp
            else:
                self.taxiTracts[line[0]]=dropoff
        #if not len(self.taxiTracts.keys())==2162:
        #    self.log.critical("number of keys in TaxiTracts should be 2162, is : {} ".format(len(self.taxiTracts.keys())))
            #exit()
    def createCrimeCT(self):
        self.mycurs.execute("""SELECT gid, pweightMay2015, pweightJun14May15, pweightJun14May15x2, pweightJun14May15x6, pweightJun14May15x12 FROM
        open.nyc_police_incident2CT_weight""")
        #TODO fix open.nyc_taxi_trips_new_june2015_censuscoutns_weight; pweight
        census=self.mycurs.fetchall()    
        for line in census:
            #list( may2015, june14-may15,  june14-may15+may15*2, june14-may15+may15*6, june14-may15+may15*12)                  
            self.crimeCT[line[0]]=[line[1], line[2], line[3], line[4], line[5]]
        if not len(self.crimeCT.keys())==2162:
            self.log.critical("number of keys in CrimeCT should be 2162, is : {} ".format(len(self.crimeCT.keys())))
            exit()
     

    def step(self, i, numSteps):
        """advance model by one step."""
        #self.log.info("time before step: {}".format(str(time.monotonic()-self.t)))
        self.modelStepCount=i
        self.generalNumSteps=numSteps
        #print('==> model step count {}'.format(self.modelStepCount))
        self.dc.collect(self)
        self.schedule.step()