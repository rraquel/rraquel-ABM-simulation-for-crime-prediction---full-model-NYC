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
from collections import Counter


class Model(mesa.Model):
    """ characteristics of the model."""
    def __init__(self, modelCfg):
        #for batch runner: instance attribute running in Model class - enables conditional shut off of the model once a condition is met.
        self.t=time.monotonic()
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
        self.targetType= modelCfg.get('targetType')
        #defines the starting location type 
        self.startLocationType= modelCfg.get('startLocationType')

        #parameters for radius search
        self.staticRadius=modelCfg.getint('staticRadius')
        self.uniformRadius=self.staticRadius*2
        self.mu=0.6
        self.dmin=2.5
        self.dmax=530
       
        #no switch case in python - can use dictionary and switch function
        self.radiusType=modelCfg.get('radiusType')

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


        self.totalRoadDistance=40986771

        self.log.info("Generating Model")

        #TODO data collection
        #collect statistics from peragent&step (can be more) - see output in model
        self.dc=DataCollector(model_reporters={
            #"modelStepCount": lambda m: m.modelStepCount,
            "agentCount":lambda m: m.schedule.get_agent_count(),
            "radiusType": lambda m: m.radiusType,
            "targetType": lambda m: m.targetType,
            "startLocation": lambda m: m.startLocationType,
            "avgSearchRadius": lambda m: sum(map(lambda a: a.searchRadius,m.schedule.agents)),
            "totalCrimes": lambda m: m.totalCrimes, 
            "totBurglary": lambda m: m.burglaryCount,
            "totRobbery": lambda m:m.robberyCount,
            "totLarceny": lambda m: m.larcenyCount,
            "totLarcenyM": lambda m: m.larcenyMCount,
            "totAssualt": lambda m: m.assualtCount,

            "totaltraveledDistance": lambda m: sum(map(lambda a: a.walkedDistance,m.schedule.agents)),

            "traveledRoads": lambda m: sum(map(lambda a: a.walkedRoads,m.schedule.agents)),
            "cummCrimes": lambda m: sum(map(lambda a: a.cummCrimes(),m.schedule.agents)),
            "uniqueCrimes": lambda m: sum(map(lambda a: a.uniqueCrimes(),m.schedule.agents)),

            "BurglaryCumm": lambda m: sum(map(lambda a: len(a.crimes[1]),m.schedule.agents)),
            "BurglaryUniq": lambda m: sum(map(lambda a: len(set(a.crimes[1])),m.schedule.agents)),
            "RobberyCumm": lambda m: sum(map(lambda a: len(a.crimes[2]),m.schedule.agents)),
            "RobberyUniq": lambda m: sum(map(lambda a: len(set(a.crimes[2])),m.schedule.agents)),
            "LarcenyCumm": lambda m: sum(map(lambda a: len(a.crimes[3]),m.schedule.agents)),
            "LarcenyUniq": lambda m: sum(map(lambda a: len(set(a.crimes[3])),m.schedule.agents)),
            "LarcenyMotorCumm": lambda m: sum(map(lambda a: len(a.crimes[5]),m.schedule.agents)),
            "LarcenyMotorUnique": lambda m: sum(map(lambda a: len(set(a.crimes[5])),m.schedule.agents)),       
            "AssaultCumm": lambda m: sum(map(lambda a: len(a.crimes[4]),m.schedule.agents)),
            "AssaultUnique": lambda m: sum(map(lambda a: len(set(a.crimes[4])),m.schedule.agents)),
           
            "cummPai2": lambda m: (((sum(map(lambda a: (a.cummCrimes()),m.schedule.agents)))/m.totalCrimes)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
            "uniqPai": lambda m: (((sum(map(lambda a: (a.uniqueCrimes()),m.schedule.agents)))/m.totalCrimes)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
             #"SD_distance": lambda m: (sqrt(lambda a: a.walkedDistance - (sum(map(a.walkedDistance,m.schedule.agents))/self.numAgents)))

            "cummPaiBurglary": lambda m: (((sum(map(lambda a: (sum(map(lambda a: len(a.crimes[1]),m.schedule.agents))),m.schedule.agents)))/m.burglaryCount)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
            "uniquePaiBurglary": lambda m: (((sum(map(lambda a: (sum(map(lambda a: len(set(a.crimes[1])),m.schedule.agents))),m.schedule.agents)))/m.burglaryCount)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
            "cummPaiRobbery": lambda m: (((sum(map(lambda a: (sum(map(lambda a: len(a.crimes[2]),m.schedule.agents))),m.schedule.agents)))/m.robberyCount)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
            "uniquePaiRobbery": lambda m: (((sum(map(lambda a: (sum(map(lambda a: len(set(a.crimes[2])),m.schedule.agents))),m.schedule.agents)))/m.robberyCount)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
            "cummPaiLarceny": lambda m: (((sum(map(lambda a: (sum(map(lambda a: len(a.crimes[3]),m.schedule.agents))),m.schedule.agents)))/m.larcenyCount)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
            "uniquePaiLarceny": lambda m: (((sum(map(lambda a: (sum(map(lambda a: len(set(a.crimes[3])),m.schedule.agents))),m.schedule.agents)))/m.larcenyCount)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
            "cummPaiLarcenyM": lambda m: (((sum(map(lambda a: (sum(map(lambda a: len(a.crimes[5]),m.schedule.agents))),m.schedule.agents)))/m.larcenyMCount)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
            "uniquePaiLarcneyM": lambda m: (((sum(map(lambda a: (sum(map(lambda a: len(set(a.crimes[5])),m.schedule.agents))),m.schedule.agents)))/m.larcenyMCount)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
            "cummPaiAssault": lambda m: (((sum(map(lambda a: (sum(map(lambda a: len(a.crimes[4]),m.schedule.agents))),m.schedule.agents)))/m.assualtCount)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
            "uniquePaiAssault": lambda m: (((sum(map(lambda a: (sum(map(lambda a: len(set(a.crimes[4])),m.schedule.agents))),m.schedule.agents)))/m.assualtCount)/(sum(map(lambda a: (a.walkedDistance+1),m.schedule.agents)))/m.totalRoadDistance) if m.modelStepCount is (m.generalNumSteps-1) else 0,
                                                       
            #"SD_distance": lambda m: (sqrt(lambda a: a.walkedDistance - (sum(map(a.walkedDistance,m.schedule.agents))/self.numAgents)))
            } ,
        agent_reporters={
            "current Road": lambda a: a.road,
            "traveledDistance": lambda a: a.walkedDistance,
            "cummCrimes": lambda m:  a.cummCrimes(),
            "uniqueCrimes": lambda m: a.uniqueCrimes(),
            "searchRadius": lambda a: a.searchRadius
            })
        
        #create roadNW
        self.G=self.createRoadNetwork()
        self.log.info("time after roadNW: {}".format(str(time.monotonic()-self.t)))
        
        #create agent
        #TODO give agent the number of steps one should move - distribution ~1-7
        #TODO include start location type (to tune starting point with PLUTO info) and demographics
        for i in range(self.numAgents):
            try:
                a=AgentX(i, self, self.radiusType, self.targetType, self.startLocationType, self.agentTravelAvg)
                self.schedule.add(a)
                #self.log.info("Offender created")
            except Exception as e:
                self.log.critical("Agents could not be created: " + str(e))
                raise SystemExit(1)
        self.log.info("{0} agents created, time {1}".format(self.numAgents,str(time.monotonic()-self.t)))

    def connectDB(self):
        try:
            self.conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
            self.mycurs=self.conn.cursor()
            #self.log.info("connected to DB")
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
        
        self.mycurs.execute("""select intersection_id,r.gid,length,crimes_2015 from 
            open.nyc_intersection2road i2r
            left join open.nyc_road_proj_final r on i2r.road_id = r. gid
            left join open.nyc_road_attributes ra on ra.road_id=r.gid""")
        #fetch all values into tuple
        interRoad=self.mycurs.fetchall()
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
            
            #add road, length and crimes as node info in graph
            #self.G.add_node(line[1], length=line[2], num_crimes=line[3])
            # TODO Parameter: Assumptions Humans walk 300 feet in 60s
            self.G.add_node(line[1],length=line[2])
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
                        self.G.add_edge(road, road2)
        self.log.debug("Number of  G: roads: {0}, intersections: {1}".format(self.G.number_of_nodes(), self.G.number_of_edges))
        self.log.debug("Isolated roads: {0}".format(len(nx.isolates(self.G))))
        #self.log.info("roadNW built, intersection size: {0}".format(len(intersect)))
        #self.log.info("roadNW built, roads size: {0}".format(self.G.number_of_nodes()))
        return self.G

    def createCrimes(self):
        self.mycurs.execute("""SELECT * from open.nyc_road2police_incident_5ft_types_Jun WHERE NOT off_type is NULL""")
        #Burglary 1, robbery 2, grand Larceny 3, assualt 4, grand larceny motor 5
        rows=self.mycurs.fetchall()
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
            crime=line[1]
            crimetype1=line[2]
            crimetype=line[3]
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
        self.allCrimes=roadCrime
    
    def createResidential(self):
        self.mycurs.execute("""select distinct(r2p.road_id),census_population_weight
            from open.nyc_road2pluto_80ft r2p left join open.nyc_pluto_areas p 
            on r2p.road_id=p.gid where census_population_weight >0 AND 
            (landuse='01' OR landuse='02'  OR landuse='03' OR landuse='04')""") 
        roads=self.mycurs.fetchall()
        self.totalresidentialRoads=len(roads)
        print(roads[0])
        roadsList=[x[0] for x in roads]
        weightList=[x[1] for x in roads if x != None]
        pWeightList=[]
        sumWeightList=sum(weightList)
        for value in weightList:
            pWeightList.append(value/sumWeightList)
        self.residentRoads=roadsList
        self.residentRoadsWeight=pWeightList


    def step(self, i, numSteps):
        """advance model by one step."""
        #self.log.info("time before step: {}".format(str(time.monotonic()-self.t)))
        self.modelStepCount=i
        self.generalNumSteps=numSteps
        #print('==> model step count {}'.format(self.modelStepCount))
        self.dc.collect(self)
        self.schedule.step()