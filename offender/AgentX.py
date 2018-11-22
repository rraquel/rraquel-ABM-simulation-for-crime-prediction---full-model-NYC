#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mesa
from mesa.time import RandomActivation
import Model
import networkx as nx
import numpy as np
import math
import sys, psycopg2, os, time, random, logging
from operator import itemgetter
from startLocation import findStartLocation
from path import Path
import globalVar


class AgentX(mesa.Agent):
    """an Agent moving"""
    def __init__(self, unique_id, model, distanceType, targetType, startLocationType, agentTravelAvg):
        super().__init__(unique_id, model)
        self.log=logging.getLogger('')
        self.unique_id=unique_id
        self.model=model
        self.conn=model.conn

        self.pos=0
        self.foundnoway=0

        #agent travel steps average until returning home
        self.agentTravelAvg=agentTravelAvg
        if agentTravelAvg is not 0:
            self.agentTravelTrip=np.random.uniform(1, (self.agentTravelAvg*2)-1)
            self.agentTravelTripList=[self.agentTravelTrip]
        else:
            self.agentTravelTrip=0
        self.log.debug('num trips travel distribution value: {}'.format(self.agentTravelTrip))
        self.tripCount=0
        self.newStart=0
        self.crimes=[]
        for i in range(6):
            self.crimes.append([])
        #list of positions offender has visited
        self.targetRoadList=[]
      
        ##select starting position by type
        self.residentRoads=model.residentRoads
        self.residentRoadsWeight=model.residentRoadsWeight
        self.startLocationType=startLocationType
        self.startRoad=findStartLocation(self.model, self.startLocationType, self.unique_id)
        self.road=self.startRoad

        #distance selection: radius or census tract
        self.distanceType=distanceType

        #selection behavior for target type
        self.targetType=targetType

        self.allCrimes=model.allCrimes
        #statistics
        #self.crimes=Counter()

        self.walkedDistance=1 #distance walked in total
        self.walkedRoads=0 
        


    def resetAgent(self):
        self.tripCount=0
        self.targetRoadList.append(self.startRoad)
        self.log.debug("reset agent")
        #TODO if agent starts at new position, need to find new start location!!!
        return self.startRoad
    
    def daytrips(self):
        """trips in one day"""
        #agent trip number drawn form distribution
        self.agentTravelTrip=np.random.uniform(1, (self.agentTravelAvg*2)-1)
        self.agentTravelTripList.append(self.agentTravelTrip)
        #make trips
        roundTravelTrip=int(round(self.agentTravelTrip))
        while self.agentTravelTrip >0 and (self.tripCount+1)<roundTravelTrip:
            #emulate do-while: assigns False for the loop to be executed before further condition testing
            print(self.road)
            f=Path(self.unique_id, self.model, self.road, self.distanceType, self.targetType, self.tripCount)
            targetRoad=f.buildpath()
            self.targetRoadList.append(targetRoad)
            self.road=targetRoad
            self.tripCount+=1
            print(targetRoad, self.tripCount, self.model.modelStepCount)
            self.log.info("agent {0}, trip count: {1}, trip avg: {2}, number of trips: {3}".format(self.unique_id, self.tripCount, self.agentTravelAvg, self.agentTravelTrip))
        self.log.debug('reset agent  {0}, trip should {1}, trip count {2}'.format(self.unique_id,self.agentTravelTrip,self.tripCount))
        #go back to starting road targetRoad=startRoad
        print(self.road)
        targetRoad=self.resetAgent()
        f=Path(self.unique_id, self.model, self.road, self.distanceType, self.targetType, self.tripCount)
        targetRoad=f.buildpathhome(self.startRoad)
        self.targetRoadList.append(targetRoad)
        print(targetRoad, self.tripCount, self.model.modelStepCount)
        self.road=targetRoad

   
    def step(self):
        """step: behavior for each offender per day, every agent starts at new position and does trips for 1 day"""
        #new day start at new location
        if self.model.modelStepCount==self.model.generalNumSteps-1:
            self.startRoad=1
            self.road=1
            self.log.debug("model needs to be run +1 step to save state of last step!!!")
            pass
        else:
            self.startRoad=findStartLocation(self.model, self.startLocationType, self.unique_id)
            self.road=self.startRoad
            self.daytrips()
            #update unique crimes done in path
            #self.log.info("agent {0}, target road list by road_id {1}".format(self.unique_id, self.targetRoadList))
        self.log.info("step done for agent {0}, time {1}".format(self.unique_id,str(time.monotonic()-self.model.t))) 
    

         
    def cummCrimes(self):
        c=0
        for i in range(len(self.crimes)):
            c += len(self.crimes[i])
        return(c)
    #unique per agent not over all the agents
    def uniqueCrimes(self):
        c=0
        for i in range(len(self.crimes)):
            c += len(set(self.crimes[i]))
        return(c)

    def cummBurglary(self):
        c=0
        c += len(self.crimes[1])
        return(c)
    def uniqBurglary(self):
        c=0
        c += len(set(self.crimes[1]))
        return(c)

    def cummRobbery(self):
        c=0
        c += len(self.crimes[2])
        return(c)
    def uniqRobbery(self):
        c=0
        c += len(set(self.crimes[2]))
        return(c)

    def cummLarceny(self):
        c=0
        c += len(self.crimes[3])
        return(c)
    def uniqLarceny(self):
        c=0
        c += len(set(self.crimes[3]))
        return(c)

    def cummLarcenyM(self):
        c=0
        c += len(self.crimes[5])
        return(c)
    def uniqLarcenyM(self):
        c=0
        c += len(set(self.crimes[5]))
        return(c)

    def cummAssault(self):
        c=0
        c += len(self.crimes[4])
        return(c)
    def uniqAssault(self):
        c=0
        c += len(set(self.crimes[4]))
        return(c)
    
