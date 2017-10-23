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
        self.crimes=[]
        for i in range(6):
            self.crimes.append([])
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
        self.staticRadius=model.staticRadius
        #uniform radius
        #minimal distance from 2.5km to foot
        self.pmin=model.dmin*3280.84
        #uniform radius: self.uniformRadius=self.staticRadius*2
        self.pmax=model.uniformRadius
        #power radius
        self.mu=model.mu
        self.dmin=model.dmin
        self.dmax=model.dmax

        self.searchRadius=self.radius()
        #selection behavior for target type
        self.targetType=targetType

        #statistics
        #self.crimes=Counter()
        self.crimesBurglary=Counter()
        self.crimesRobbery=Counter()
        self.crimesLarceny=Counter()
        self.crimesAssault=Counter()
        self.crimesLarcenymotor=Counter()

        #self.uniqueCrimes=0
        #self.cummCrimes=0
        self.walkedDistance=0 #distance walked in total
        #TODO create array with initial position and all targets?
        self.walkedRoads=0 
        
        self.log=logging.getLogger('')


    def findStartLocation(self):
        startRoad=getattr(self, self.model.startLocationType)()
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

    def radius(self):
        print('radius')
        return(getattr(self, self.model.radiusType)())

    def staticR(self):
        self.log.info("static radius Agent")
        return self.staticRadius

    def uniformR(self):
        #minimal distance from 2.5km to foot
        radius=np.random.uniform(self.pmin, self.pmax)
        self.log.info("uniform radius Agent: {}".format(radius))
        return (np.random.uniform(self.pmin, self.pmax))

    def powerR(self):
        beta=1+self.mu
        pmax = math.pow(self.dmin, -beta)
        pmin = math.pow(self.dmax, -beta)
        uniformProb=np.random.uniform(pmin, pmax)
        #levy flight: P(x) = Math.pow(x, -1.59) - find out x? given random probability within range
        powerKm =  (1/uniformProb)*math.exp(1/beta)
	    #levy flight gives distance in km - transform km to foot
        radius=powerKm * 3280.84
        self.log.debug("power search radius: {0}".format(round(radius,0)))
        return radius

    def weightedChoice(self, roads, road):
        #TODO bring weihts to same scale!!!
        if not roads:
            self.log.critical('no roads, probably target venue has no road: {}'.format(road))
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
                        as fs left join open.nyc_road2fs_near r2f on r2f.fs_id=fs.venue_id 
                        where not road_id is null""".format(road,maxRadius,minRadius))
                    roads=mycurs.fetchall() #returns tuple of tuples, venue_id and road_id paired
                else:
                    mycurs.execute("""select road_id from (
                        select venue_id from open.nyc_fs_venue_join where st_dwithin( (
                            select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {1})
                            and not st_dwithin( (
                                select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {2}))
                                as fs left join open.nyc_road2fs_near r2f on r2f.fs_id=fs.venue_id 
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
                    AS fs LEFT JOIN open.nyc_road2fs_near r2f on r2f.fs_id=fs.venue_id WHERE NOT road_id is null"""
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
                    AS fs LEFT JOIN open.nyc_road2fs_near r2f on r2f.fs_id=fs.venue_id WHERE NOT road_id is null"""
                    .format(road,maxRadius,minRadius))
                    roads=mycurs.fetchall() #returns tuple of tuples, venue_id,weighted_checkins
            roadId=self.weightedChoice(roads, road)
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
    
    def crimesOnRoad (self, road):
        mycurs = self.conn.cursor()
        mycurs.execute("""SELECT object_id, off_type from open.nyc_road2police_incident_5ft_types WHERE road_id ={}"""
        .format(road))
        rows=mycurs.fetchall()          
        for crime in rows:
            crimetype=crime[1]
            self.crimes[crimetype].append(crime[0])

    def findMyWay(self, targetRoad):
        self.log.debug('search radius: {}'.format(self.searchRadius))
        try:
            #roads are represented as nodes in G
            self.way=nx.shortest_path(self.model.G,self.road,targetRoad,weight='length')
            #print("Agent ({0}) way: {1}".format(self.unique_id,self.way))
            for road in self.way:
                self.walkedDistance += self.model.G.node[road]['length']
                self.crimesOnRoad(road)
                self.walkedRoads +=1
        except Exception as e:
            self.log.warning("Error: One agent found no way: agent id {0}, startRoad: {1}, targetRoad {2} ".format(self.unique_id, self.startRoad, targetRoad))
            self.way=[self.road,targetRoad]
    
    def step(self):
        """step: behavior for each offender"""
        #print('start road: {}'.format(self.road))
        #select new radius for power-law
        #uniform distr. radius
        self.searchRadius=self.radius()
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
        #self.cummCrimes=sum(self.crimes.val
        #self.uniqueCrimes=len(list(self.crimes))
        self.log.info("agent {0}, target road list by road_id {1}".format(self.unique_id, self.targetRoadList))
        self.log.info("step done for agent {0}".format(self.unique_id))
    
    def cummCrimes(self):
        c=0
        for i in range(len(self.crimes)):
            c += len(self.crimes[i])
        return(c)

    def uniqueCrimes(self):
        c=0
        for i in range(len(self.crimes)):
            c += len(set(self.crimes[i]))
        return(c)