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
from collections import Counter

class AgentX(mesa.Agent):
    """an Agent moving"""
    def __init__(self, unique_id, model, radiusType, targetType, startLocationType, agentTravelAvg, centerAttract):
        super().__init__(unique_id, model)
        self.log=logging.getLogger('')
        self.pos=0

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

        #list of positions offender has visited
        self.targetRoadList=[]
        
        self.conn=model.conn
      
        
        ##select starting position by type
        self.startLocationType=startLocationType
        self.startRoad=self.findStartLocation()
        self.road=self.startRoad

        #attractiveness of city center
        self.centerAttract=centerAttract

        #selection behavior for radius type
        #static
        self.radiusType=radiusType

        if radiusType is 0 :
            self.searchRadius=model.staticRadius
            self.log.info("static radius Agent")
        #uniform
        elif radiusType is 1 :
            #minimal distance from 2.5km to foot
            self.pmin=model.dmin*3280.84
            #uniform radius: self.uniformRadius=self.staticRadius*2
            self.pmax=model.uniformRadius
            self.searchRadius=np.random.uniform(self.pmin, self.pmax)
            #print('uniformProbability number: {}'.format(uniformProb))
            self.log.info("uniform radius Agent")
        #power
        elif radiusType is 2 :
            self.mu=model.mu
            self.dmin=model.dmin
            self.dmax=model.dmax
            self.searchRadius=self.powerRadius(self.mu, self.dmin, self.dmax)
            self.log.info("power radius Agent is {}".format(self.searchRadius))    
        #selection behavior for target type
        self.targetType=targetType

        #statistics
        self.crimes=Counter()
        self.crimesBurglary=Counter()
        self.crimesRobbery=Counter()
        self.crimesLarceny=Counter()
        self.crimesAssault=Counter()
        self.crimesLarcenymotor=Counter()
        self.crimesRape=Counter()

        self.uniqueCrimes=0
        self.cummCrimes=0
        self.walkedDistance=0 #distance walked in total
        #TODO create array with initial position and all targets?
        self.walkedRoads=0 
        
        self.log=logging.getLogger('')

    def findStartLocation(self):
        if self.startLocationType is 0:
            startRoad=self.findStartRandom()
        elif self.startLocationType is 1:
            startRoad=self.findStartResidence()
        else:
            #defalut
            startRoad=self.findStartRandom()
            self.log.critical("Start location type is out of range: {}".format(self.startLocationType))
        self.log.debug("startRaod: {0}".format(startRoad))
        self.targetRoadList.append(startRoad)
        return startRoad
        
    def findStartRandom(self):
        """select startingPoint from random sample of nodes"""
        return random.sample(self.model.G.nodes(),1)[0]

    def findStartResidence(self):
        """Select startRoad within Residential Areas from PlutoMap"""
        #TODO change nyc_road2pluto and query
        mycurs = self.model.conn.cursor()
        mycurs.execute("""select distinct(r2p.road_id) from open.nyc_road2pluto_80ft r2p
                left join open.nyc_pluto_areas p on r2p.gid = p.gid""")
        starts = mycurs.fetchall()
        startRoadTuple=random.choice(starts)
        startRoad=startRoadTuple[0]
        self.log.debug('start road in PLUTO: {}'.format(startRoad))
        return startRoad

    def resetAgent(self):
        self.tripCount=0
        self.targetRoadList.append(self.startRoad)
        self.log.debug("reset agent")
        return self.startRoad

    def weightedChoice(self, roads):
        #TODO bring weihts to same scale!!!
        if not roads:
            self.log.critical('no roads, probably target venue has no road')
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
                self.log.debug('combined weights: {}'.format(weightList[0]))
            pWeightList=[]
            sumWeightList=sum(weightList)
            for value in weightList:
                pWeightList.append(value/sumWeightList)
            self.log.debug('weightlist p sum: {}'.format(sum(pWeightList)))
            roadIdNp=np.random.choice(roadsList, 1, True, pWeightList)
            roadId=roadIdNp[0]  
        return roadId


    def searchTarget(self, road, searchRadius):
        if road is None:
            road=self.startRoad
        #print('in searchTarget: current road for new target: {0}'.format(road))
        mycurs = self.conn.cursor()
        targetRoad=0
        #5% boundry
        maxRadius=searchRadius*1.025
        #in repast it was set to 0.925 - error
        minRadius=searchRadius*0.975
        count=0
        roadId=None
        while targetRoad==0:
            count+=1
            #print('search target road iteration {}'.format(count))
            #print('target type: {0}'.format(self.targetType))
            #select target depending on targetType: 0: Random ROAD, 1: Random VENUE, 2: Popular Venue
            if self.targetType is 0:
                if self.centerAttract is 1:
                    mycurs.execute("""select gid,weight_center from (
                        select gid,weight_center,geom from open.nyc_road_weight_to_center where st_dwithin(
                        (select geom from open.nyc_road_weight_to_center where gid={0}),geom,{1})
                        and not st_dwithin((select geom from open.nyc_road_weight_to_center where gid={0}) ,geom,{2})
                        ) as bar;""".format(road,maxRadius,minRadius))
                    roads=mycurs.fetchall() #returns tuple with first row (unordered list)
                else:
                    mycurs.execute("""select gid from (
                        select gid,weight_center,geom from open.nyc_road_weight_to_center where st_dwithin(
                        (select geom from open.nyc_road_weight_to_center where gid={0}),geom,{1})
                        and not st_dwithin((select geom from open.nyc_road_weight_to_center where gid={0}) ,geom,{2})
                        ) as bar;""".format(road,maxRadius,minRadius))
                    roads=mycurs.fetchall() #returns tuple with first row (unordered list)
            elif self.targetType is 1:
                if self.centerAttract is 1:
                    mycurs.execute("""select road_id, weight_center from (
                        select venue_id,weight_center from open.nyc_fs_venue_join_weight_to_center WHERE st_dwithin( (
                        select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {1})
                        and not st_dwithin( (
                        select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {2}))
                        as fs left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                        where not road_id is null""".format(road,maxRadius,minRadius))
                    roads=mycurs.fetchall() #returns tuple of tuples, venue_id and road_id paired
                else:
                    mycurs.execute("""select road_id from (
                        select venue_id from open.nyc_fs_venue_join where st_dwithin( (
                            select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {1})
                            and not st_dwithin( (
                                select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {2}))
                                as fs left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                                where not road_id is null""".format(road,maxRadius,minRadius))
                    roads=mycurs.fetchall() #returns tuple of tuples, venue_id and road_id paired
            elif self.targetType is 2:
                if self.centerAttract is 1:
                    mycurs.execute("""SELECT road_id, weight_center, weighted_checkins FROM(
                    SELECT venue_id, weight_center, checkins_count,(checkins_count * 100.0)/temp.total_checkins as weighted_checkins
                    from (SELECT COUNT(venue_id)as total_venues, SUM(checkins_count) as total_checkins FROM open.nyc_fs_venue_join
                    where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
                    and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2})
                    ) as temp, open.nyc_fs_venue_join_weight_to_center
                    where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
                    and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2}))
                    AS fs LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id WHERE NOT road_id is null"""
                    .format(road,maxRadius,minRadius))
                    roads=mycurs.fetchall() #returns tuple of tuples, venue_id,weighted_checkins
                else:
                    #TODO until venues mapping is cleared !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    mycurs.execute("""SELECT road_id, weighted_checkins FROM(
                    SELECT venue_id, checkins_count,(checkins_count * 100.0)/temp.total_checkins as weighted_checkins
                    from (SELECT COUNT(venue_id)as total_venues, SUM(checkins_count) as total_checkins FROM open.nyc_fs_venue_join
                    where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
                    and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2})
                    ) as temp, open.nyc_fs_venue_join
                    where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
                    and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2}))
                    AS fs LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id WHERE NOT road_id is null"""
                    .format(road,maxRadius,minRadius))
                    roads=mycurs.fetchall() #returns tuple of tuples, venue_id,weighted_checkins
            roadId=self.weightedChoice(roads)
            if not roadId is None:
                targetRoad=roadId
                #print("roadid in target: {0}".format(roadId[0]))
                self.targetRoadList.append(targetRoad)
                return (targetRoad)
            #enlarge by 10%
            maxRadius+=maxRadius*0.025
            minRadius-=minRadius*0.025
            if count>1:
                self.log.debug('radius enlarge count: {}'.format(count))
            return targetRoad
    
    def crimesOnRoad (self, road, type):
        mycurs = self.conn.cursor()
        if type is 0:
            mycurs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft WHERE road_id ={}"""
            .format(road))
        if type is 1:
            mycurs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_BURGLARY WHERE road_id ={}"""
            .format(road))
        elif type is 2:
            mycurs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_ROBBERY WHERE road_id ={}"""
            .format(road))
        elif type is 3:
            mycurs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_LARCENY WHERE road_id ={}"""
            .format(road))
        elif type is 4:
            mycurs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_ASSAULT WHERE road_id ={}"""
            .format(road))
        elif type is 5:
            mycurs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_LARCENY_MOTOR WHERE road_id ={}"""
            .format(road))
        elif type is 6:
            mycurs.execute("""SELECT object_id from open.nyc_road2police_incident_5ft_RAPE WHERE road_id ={}"""
            .format(road))
        crimes=mycurs.fetchall()
        crimes2=[]
        for crime in crimes:
            crimes2.append(crime[0])
        #self.log.debug('crimes2: {0}, length: {1}'.format(crimes2, len(crimes2)))
        return crimes2

    def findMyWay(self, targetRoad):
        self.log.debug('search radius: {}'.format(self.searchRadius))
        try:
            #roads are represented as nodes in G
            self.way=nx.shortest_path(self.model.G,self.road,targetRoad,weight='length')
            #print("Agent ({0}) way: {1}".format(self.unique_id,self.way))
            for road in self.way:
                self.walkedDistance += self.model.G.node[road]['length']
                #crimes=Counter(self.crimesOnRoad(road, 0)
                self.crimes+=Counter(self.crimesOnRoad(road, 0))
                self.crimesBurglary+=Counter(self.crimesOnRoad(road, 1))
                self.crimesRobbery+=Counter(self.crimesOnRoad(road, 2))
                self.crimesLarceny+=Counter(self.crimesOnRoad(road, 3))
                self.crimesAssault+=Counter(self.crimesOnRoad(road, 4))
                self.crimesLarcenymotor+=Counter(self.crimesOnRoad(road, 5))
                self.crimesRape+=Counter(self.crimesOnRoad(road, 6))
                self.walkedRoads +=1
        except Exception as e:
            self.log.warning("Error: One agent found no way: agent id {0}, startRoad: {1}, targetRoad {2} ".format(self.unique_id, self.startRoad, targetRoad))
            self.way=[self.road,targetRoad]
        

    def powerRadius(self, mu, dmin, dmax):
        beta=1+mu
        pmax = math.pow(dmin, -beta)
        pmin = math.pow(dmax, -beta)
        uniformProb=np.random.uniform(pmin, pmax)
        #levy flight: P(x) = Math.pow(x, -1.59) - find out x? given random probability within range
        powerKm =  (1/uniformProb)*math.exp(1/beta)
	    #levy flight gives distance in km - transform km to foot
        powerRadius = powerKm * 3280.84
        self.log.debug("power search radius: {0}".format(round(powerRadius,0)))
        return powerRadius

    
    def step(self):
        """step: behavior for each offender"""
        #print('start road: {}'.format(self.road))
        #select new radius for power-law
        #uniform distr. radius
        if self.radiusType is 1:
            self.searchRadius=np.random.uniform(self.pmin, self.pmax)
            #print('next uniform distr. radius {0}'.format(self.radiusType))
            #power radius
        if self.radiusType is 2:
            self.searchRadius=self.powerRadius(self.mu, self.dmin, self.dmax)
            #print('next power radius {0}'.format(self.radiusType))
        #rest agent to start at new location
        if self.newStart is 1:
            self.startRoad=self.findStartLocation()
            self.log.debug("new start road: {}".format(self.startRoad))
            targetRoad=self.startRoad
            self.agentTravelTrip=np.random.uniform(1, (self.agentTravelAvg*2)-1)
            self.agentTravelTripList.append(self.agentTravelTrip)
            self.log.debug("agent {0} travel trip count list {1}".format(self.unique_id,self.agentTravelTripList))
            self.newStart=0
            self.tripCount=0
        #last step before agent starts at new location
        if self.agentTravelTrip >0 and (self.tripCount+1)>self.agentTravelTrip:
            targetRoad=self.resetAgent()
            self.newStart=1
            self.tripCount+=1
            self.findMyWay(targetRoad)
            self.log.debug("target road in reset Agent is: {}".format(targetRoad))
        #normal step for agent to find target and way
        else:
            #one step: walk to destination
            targetRoad=self.searchTarget(self.road, self.searchRadius)
            self.tripCount+=1
            self.log.info("agent {0}, trip count: {1}, trip avg: {2}, number of trips: {3}".format(self.unique_id, self.tripCount, self.agentTravelAvg, self.agentTravelTrip))
            self.findMyWay(targetRoad)
        self.road=targetRoad
        self.cummCrimes=sum(self.crimes.values())
        self.uniqueCrimes=len(list(self.crimes))
        self.log.info("agent {0}, target road list by road_id {1}".format(self.unique_id, self.targetRoadList))
        self.log.info("step done for agent {0}".format(self.unique_id))