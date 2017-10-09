#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mesa
from mesa.time import RandomActivation
import Model
import networkx as nx
import numpy as np
import math
import sys, psycopg2, os, time, random, logging
from random import choices
from operator import itemgetter

class AgentX(mesa.Agent):
    """an Agent moving"""
    def __init__(self, unique_id, model, radiusType, targetType, startLocationType, agentReturn):
        super().__init__(unique_id, model)
        self.pos=0

        #agent travel steps average until returning home
        self.agentReturn=agentReturn
        self.agentTravelAvg=model.agentTravelAvg     

        #list of positions offender has visited
        self.targetRoadList=[]

        #start location choice
        self.startLocationType=startLocationType
        self.startRoad=self.newAgent(model)
        self.road=self.startRoad
        self.conn=model.conn
        

        #select starting position by type

        #selection behavior for radius type
        #static
        if radiusType is 0 :
            self.searchRadius=model.staticRadius
            print('static radius Agent')
        #uniform
        elif radiusType is 1 :
            #minimal distance from 2.5km to foot
            self.pmin=model.dmin*3280.84
            #uniform radius: self.uniformRadius=self.staticRadius*2
            self.pmax=model.uniformRadius
            self.searchRadius=np.random.uniform(self.pmin, self.pmax)
            #print('uniformProbability number: {}'.format(uniformProb))
            print('uniform radius Agent')
        #power
        elif radiusType is 2 :
            self.mu=model.mu
            self.dmin=model.dmin
            self.dmax=model.dmax
            self.searchRadius=self.powerRadius(self.mu, self.dmin, self.dmax)
            print('power radius Agent is {0}'.format(self.searchRadius))
        self.radiusType=radiusType

        #selection behavior for target type
        self.targetType=targetType

        #statistics
        self.seenCrimes=0 #historic crimes passed on path
        self.walkedDistance=0 #distance walked in total
        self.crimesUnique = set() # List of seen crimes (ids)
        #TODO create array with initial position and all targets?
        self.walkedRoads=0 
        
        self.log=logging.getLogger('')
    
    def newAgent (self, model):
        self.startRoad=self.findStartLocation(model)
        print('new start road: {}'.format(self.startRoad))
        if self.agentReturn is 1:
            self.agentTravelTrips=np.random.uniform(1, (self.agentTravelAvg*2)-1)
            print('new uniform trip travel distribution value: {}'.format(self.agentTravelTrips))
        self.tripCount=0
        self.newStart=0
        return self.startRoad

    def returnAgent(self):
        self.targetRoadList.append(self.startRoad)
        print('reset agent')
        return self.startRoad


    def findStartLocation(self, model):
        if self.startLocationType is 0:
            startRoad=self.findStartRandom(model)
        elif self.startLocationType is 1:
            startRoad=self.findStartResidence()
        else:
            #defalut
            startRoad=self.findStartRandom(model)
        print("startRoad: {0}".format(startRoad))
        self.targetRoadList.append(startRoad)
        return startRoad
        
    def findStartRandom(self, model):
        """select startingPoint from random sample of nodes"""
        return random.sample(model.G.nodes(),1)[0]

    def findStartResidence(self):
        """Select startRoad within Residential Areas from PlutoMap"""
        #TODO change nyc_road2pluto and query
        mycurs = self.model.conn.cursor()
        mycurs.execute("""select distinct(r2p.road_id) from open.nyc_road2pluto_80ft r2p
                left join open.nyc_pluto_areas p on r2p.gid = p.gid""")
        starts = mycurs.fetchall()
        startRoadTuple=random.choice(starts)
        startRoad=startRoadTuple[0]
        #print('start road in PLUTO: {}'.format(startRoad))
        return startRoad

    def searchTarget(self, road, searchRadius):
        if road is None:
            road=self.startRoad
        #print('in searchTarget: current road for new target: {0}'.format(road))
        mycurs = self.conn.cursor()
        targetRoad=0
        maxRadius=searchRadius*1.025
        #in repast it was set to 0.925 - error
        minRadius=searchRadius*0.975
        count=0
        while targetRoad==0:
            count+=1
            #print('search target road iteration {}'.format(count))
            #print('target type: {0}'.format(self.targetType))
            #select target depending on targetType: 0: Random ROAD, 1: Random VENUE, 2: Popular Venue
            if self.targetType is 0:
                mycurs.execute("""select gid from (
                    select gid,geom from open.nyc_road_proj_final where st_dwithin(
                    (select geom from open.nyc_road_proj_final where gid={0}),geom,{1})
                    and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}) ,geom,{2})
                    ) as bar;""".format(road,maxRadius,minRadius))
                roads=mycurs.fetchall() #returns tuple with first row (unordered list)
                roadTuple=random.choice(roads)
                roadId=roadTuple[0]
            elif self.targetType is 1:
                mycurs.execute("""select venue_id,road_id from (
                    select venue_id from open.nyc_fs_venue_join where st_dwithin( (
                        select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {1})
                        and not st_dwithin( (
                            select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {2}))
                            as fs left join open.nyc_road2fs_80ft r2f on r2f.location_id=fs.venue_id 
                            where not road_id is null""".format(road,maxRadius,minRadius))
                venues=mycurs.fetchall() #returns tuple of tuples, venue_id and road_id paired
                venueId=random.choice(venues) #selects a random element of the tuple
                print('venue element: {}'.format(venueId))
                roadId=venueId[1] #selects the road_id from the chosen tuple
            elif self.targetType is 2:
                #TODO until venues mapping is cleared !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                roadId=None
                count2=0
                #orders query result by checkis_count
                mycurs.execute("""SELECT venue_id, road_id, checkins_count, weighted_checkins FROM(
                SELECT venue_id, checkins_count,(checkins_count * 100.0)/temp.total_checkins as weighted_checkins
                from (SELECT COUNT(venue_id)as total_venues, SUM(checkins_count) as total_checkins FROM open.nyc_fs_venue_join
                where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
                and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2})
                ) as temp, open.nyc_fs_venue_join
                where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
                and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2}))
                AS fs LEFT JOIN open.nyc_road2fs_80ft r2f on r2f.location_id=fs.venue_id WHERE NOT road_id is null"""
                .format(road,maxRadius,minRadius))
                venues=mycurs.fetchall() #returns tuple of tuples, venue_id,weighted_checkins
                # can add - but may take up more time: order by weighted_checkins desc
                #print("venues in priority: {}".format(venues[(len(venues))-1]))
                #venuesSort=sorted(venues, key=itemgetter(2))
                #print("venues in priority: {}".format(venuesSort[0]))
                #venueId=random.choice(venues) #selects a random element of the tuple
                #for random.choices weights= need a list of the weights - therefore convert weights to list using list comprehension
                weightsList=[x[1] for x in venues]
                #convert float to integer
                weightsListInt = list(map(int, weightsList))
                #print('venue weights list : {}'.format(weightsList[0]))
                #print('venue weights list : {}'.format(weightsListInt[0]))
                venue=choices(venues, weights=weightsListInt, cum_weights=None, k=1)
                #print('venue id: {}'.format(type(venue)))
                #print('venue id: {}'.format(venue[0][0]))
                mycurs.execute("""SELECT road_id, venue_id FROM (SELECT venue_id FROM open.nyc_fs_venue_join WHERE venue_id={0})
                AS fs LEFT JOIN open.nyc_road2fs_80ft r2f ON r2f.location_id=fs.venue_id"""
                .format(venue[0][0])
                )
                roadIds=mycurs.fetchall()
                #print('fetchall type roadId from popular venues: {}'.format(type(roadIds)))
                roadIdTuple=random.choice(roadIds) #selects the road_id from the possible roads for the venue - it is a list (one element only) of tuples (road_id - venue_id)
                roadId=roadIdTuple[0]
                #print('roadId from popular venues: {0} with type: {1}'.format(roadId, type(roadId)))
            else:
            #selects all roads that have points within the radius
                self.log.error("targetType not within range: "+self.targetType)
            #print('new target road is: {}'.format(roadId))
            if not roadId is None:
                targetRoad=roadId
                #print("roadid in target: {0}".format(roadId[0]))
                self.targetRoadList.append(targetRoad)
                return (targetRoad)
            searchRadius=searchRadius/10
            return targetRoad
        
    def findMyWay(self, targetRoad):
        try:
            #roads are represented as nodes in G
            self.way=nx.shortest_path(self.model.G,self.road,targetRoad,weight='length')
            #print("Agent ({0}) way: {1}".format(self.unique_id,self.way))
        except Exception as e:
            print ("Error: One agent found no way: ",e,self.unique_id)
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
        print ("power search radius: {0}".format(round(powerRadius,0)))
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
            self.startRoad=newAgent(model)
            print('Agent new start, print newstart, should be set to 0 {}'.format(newStart))
        #last step before agent starts at new location
        if self.agentReturn is 1 and (self.tripCount+1)>self.agentTravelTrips:
            targetRoad=self.returnAgent()
            self.newStart=1
            self.tripCount+=1
            self.findMyWay(targetRoad)
            print('target road in reset Agent is: {}'.format(targetRoad))
        #normal step for agent to find target and way
        else:
            #one step: walk to destination
            targetRoad=self.searchTarget(self.road, self.searchRadius)
            self.tripCount+=1
            print('agent {0}, trip count: {1}, trip avg: {2}'.format(self.unique_id, self.tripCount, self.agentTravelAvg))
            self.findMyWay(targetRoad)
        for road in self.way:
            self.walkedDistance += self.model.G.node[road]['length']
            self.seenCrimes += self.model.G.node[road]['num_crimes']
            self.walkedRoads +=1
            self.crimesUnique = self.model.G.node[road]['crimesList']
        self.road=targetRoad
        print('agent {0}, target road list by road_id {1}'.format(self.unique_id, self.targetRoadList))
        print('step done for agent {0}'.format(self.unique_id))