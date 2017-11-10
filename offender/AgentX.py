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
import globalVar


class AgentX(mesa.Agent):
    """an Agent moving"""
    def __init__(self, unique_id, model, radiusType, targetType, startLocationType, agentTravelAvg):
        super().__init__(unique_id, model)
        self.log=logging.getLogger('')
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
        
        self.conn=model.conn
      
        ##select starting position by type
        self.residentRoads=model.residentRoads
        self.residentRoadsWeight=model.residentRoadsWeight
        self.startLocationType=startLocationType
        self.startRoad=0
        self.road=0

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

        self.allCrimes=model.allCrimes
        #statistics
        #self.crimes=Counter()

        self.walkedDistance=1 #distance walked in total
        #TODO create array with initial position and all targets?
        self.walkedRoads=0 
        
        self.log=logging.getLogger('')


    def findStartLocation(self):
        access=False
        loopCount=0
        while access==False:
                loopCount+=1
                startRoad=getattr(self, self.model.startLocationType)()
                access=self.roadAccessibility(startRoad)
                self.log.debug('test of while loop in start {}'.format(loopCount))
        self.log.debug("startRoad: {0}".format(startRoad))
        self.targetRoadList.append(startRoad)
        return startRoad
        
    def findStartRandom(self):
        """select startingPoint from random sample of nodes"""
        return random.choice(self.model.G.nodes(),1)[0]

    def findStartResidence(self):
        """Select startRoad within Residential Areas from PlutoMap"""
        self.log.debug('weightlist p sum: {}'.format(sum(pWeightList)))
        roadIdNp=np.random.choice(self.residentRoads,1)
        startRoad=roadIdNp[0]
        return startRoad

    def findStartResidencePopulation(self):
        """Select startRoad within Residential Areas from PlutoMap and population density"""
        roadIdNp=np.random.choice(self.residentRoads, 1, True, self.residentRoadsWeight)
        startRoad=roadIdNp[0]
        return startRoad

    def resetAgent(self):
        self.tripCount=0
        self.targetRoadList.append(self.startRoad)
        self.log.debug("reset agent")
        return self.startRoad

    def radius(self):
        return(getattr(self, self.model.radiusType)())

    def staticR(self):
        self.log.info("static radius Agent")
        return self.staticRadius

    def uniformR(self):
        #minimal distance from 2.5km to foot
        radius=np.random.uniform(self.pmin, self.pmax)
        #self.log.info("uniform radius Agent: {}".format(radius))
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
        self.log.debug("power search radius: {0}".format(round(radius)))
        #print(round(radius))
        return round(radius)

    def findTargetByType(self, road, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        return(getattr(self, self.model.targetType)(road, mycurs, maxRadius, minRadius))

    def randomRoad(self, road, mycurs, maxRadius, minRadius):
        mycurs.execute("""select gid from (
            select gid,geom from open.nyc_road_weight_to_center where st_dwithin(
            (select geom from open.nyc_road_weight_to_center where gid={0}),geom,{1})
            and not st_dwithin((select geom from open.nyc_road_weight_to_center where gid={0}) ,geom,{2})
            ) as bar;""".format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple with first row (unordered list)
        self.log.debug('random Road')
        return roads

    def randomRoadCenter(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        mycurs.execute("""select gid,weight_center from (
            select gid,weight_center,geom from open.nyc_road_weight_to_center where st_dwithin(
            (select geom from open.nyc_road_weight_to_center where gid={0}),geom,{1})
            and not st_dwithin((select geom from open.nyc_road_weight_to_center where gid={0}) ,geom,{2})
            ) as bar;""".format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple with first row (unordered list)
        #self.log.debug('random Road Center')
        return roads

    def randomVenue(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        mycurs.execute("""select road_id from (
            select venue_id from open.nyc_fs_venue_join where st_dwithin( (
            select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {1})
            and not st_dwithin( (
            select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {2}))
            as fs left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
            where not road_id is null""".format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple of tuples, venue_id and road_id paired
        self.log.debug('random Venue')        
        return roads    

    def randomVenueCenter(self, road, mycurs,  maxRadius, minRadius):
        mycurs = self.conn.cursor()
        #venues venue_id=270363 or venue_id=300810 are incorrectly mapped and therefore have weihgt=0, should not be accoutned for
        mycurs.execute("""select road_id, weight_center from (
            select venue_id,weight_center from open.nyc_fs_venue_join_weight_to_center WHERE st_dwithin( (
            select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {1})
            and not st_dwithin( (
            select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {2}))
            as fs left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
            where not road_id is null and not weight_center=0""".format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple of tuples, venue_id and road_id paired
        #self.log.debug('random Venue Center')        
        return roads

    def popularVenue(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        mycurs.execute("""SELECT road_id, checkins_count FROM(
            SELECT venue_id, checkins_count
            from open.nyc_fs_venue_join
            where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
            and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2}))
            AS fs LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id WHERE NOT road_id is null"""
            .format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple of tuples, venue_id,weighted_checkins
        self.log.debug('popular Venue') 
        return roads

    def popularVenueCenter(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        #venues venue_id=270363 or venue_id=300810 are incorrectly mapped and therefore have weihgt=0, should not be accoutned for
        mycurs.execute("""SELECT road_id, weight_center, checkins_count FROM(
            SELECT venue_id, weight_center, checkins_count
            from open.nyc_fs_venue_join_weight_to_center
            where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
            and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2}))
            AS fs LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id WHERE NOT road_id is NULL AND NOT weight_center=0"""
            .format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple of tuples, venue_id,weighted_checkins
        self.log.debug('popular Venue Center') 
        return roads

    def searchTarget(self, road, searchRadius):
        """search target within radius"""
        if road is None:
            road=self.startRoad
        #print('in searchTarget: current road for new target: {0}'.format(road))
        targetRoad=0
        count=0
        roadId=None
        #5% boundry ~0.6 km
        maxRadius=searchRadius*1.025
        #in repast it was set to 0.925 - error
        minRadius=searchRadius*0.975
        while targetRoad==0:
            count+=1
            roads=self.findTargetByType(road, maxRadius, minRadius)
            roadId=self.weightedChoice(roads, road)
            if not roadId is None:
                targetRoad=roadId
                self.targetRoadList.append(targetRoad)
                return (targetRoad)
            #enlarge by 10%
            maxRadius=maxRadius*1.05
            minRadius=minRadius*0.95
            if count>1:
                searchRadius=self.radius()
                maxRadius=searchRadius*1.025
                minRadius=searchRadius*0.975
                self.log.debug('new radius: {}'.format(self.searchRadius))
            elif count>5:
                targetRoad=self.startRoad
                self.log.critical("5 radius didn't work: targetroad=startRoad: agent id {0}, startRoad: {1}, current road: {3} targetRoad {2} , radius {3}".format(self.unique_id, self.startRoad, targetRoad, self.road, self.radius))
            elif count>7:
                targetRoad=self.targetRoadList[-2]
            elif count>8:
                targetRoad=self.targetRoadList[-3]
        return targetRoad

    def weightedChoice(self, roads, road):
        """choice of target by weighting if avalable"""
        #TODO bring weihts to same scale!!!
        if not roads:
            self.log.debug('no roads in radius, road {0}, search radius: {1}, radiustype: {2}'.format(road, self.searchRadius, self.radiusType))
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
                weightList2=[i for i in weightList2]
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
    
       
    def crimesOnRoad(self, road):
        """counts crimes found on each road"""
        try:
            attributList=self.allCrimes[road]
            for item in attributList:
                crimetype=item[1]
                crime=item[0]
                globalVar.crimesUniqueOverall.add(crime)
                self.crimes[crimetype].append(crime)
            #print('crimesUniqueOverall print {}'.format(globalVar.crimesUniqueOverall))   
        except:
            #self.log.debug("road has no crime")
            pass

     #unique over all agents       
    def uniqueCrimesOverall(self):
        """saves crime id over all the agents in global variable"""
        for i in range(len(self.crimes)):
            #in set(): add is for single value and update for list of values
            globalVar.burglaryUniqueOverall.update(self.crimes[1])
            globalVar.robberyUniqueOverall.update(self.crimes[2])
            globalVar.larcenyUniqueOverall.update(self.crimes[3])
            globalVar.larcenyMUniqueOverall.update(self.crimes[5])
            globalVar.assualtUniqueOverall.update(self.crimes[4])         

    def findMyWay(self, targetRoad):
        """find way to target road and count statistics for path"""
        #self.log.debug('search radius: {}'.format(self.searchRadius))
        try:
            #roads are represented as nodes in G
            self.way=nx.shortest_path(self.model.G,self.road,targetRoad,weight='length')
            #print("Agent ({0}) way: {1}".format(self.unique_id,self.way))
            for road in self.way:
                self.walkedDistance += self.model.G.node[road]['length']
                self.crimesOnRoad(road)
                self.walkedRoads +=1
                sql = """insert into open.res_la_roads ("id","run_id","step","agent","road_id") values
                    (DEFAULT,{0},{1},{2},{3} )""".format(self.model.run_id, self.model.modelStepCount, self.unique_id, road)
                #Remove if not DB writing-
                self.model.mycurs.execute(sql)
            self.foundnoway=0
        except Exception as e:
            self.log.critical("trip: Error: One agent found no way: agent id {0}, startRoad: {1}, current road: {3} targetRoad {2} , radius {3}".format(self.unique_id, self.startRoad, targetRoad, self.road, self.radius))
            #erases target from targetList

    def roadAccessibility(self, targetRoad):
        """test if there is a way to the road"""
        try:
            self.way=nx.shortest_path(self.model.G,7,targetRoad)
            return True
        except:
            return False
        
    def daytrips(self):
        """trips in one day"""
        self.searchRadius=self.radius()
        #agent trip number drawn form distribution
        self.agentTravelTrip=np.random.uniform(1, (self.agentTravelAvg*2)-1)
        self.agentTravelTripList.append(self.agentTravelTrip)
        #make trips
        roundTravelTrip=int(round(self.agentTravelTrip))
        while self.agentTravelTrip >0 and (self.tripCount+1)<roundTravelTrip:
            loopCount=0
            #emulate do-while: assigns False for the loop to be executed before further condition testing
            access=False
            while access==False:
                loopCount+=1
                targetRoad=self.searchTarget(self.road, self.searchRadius)
                if loopCount==6:
                    targetRoad=self.targetRoadList[-2]
                elif loopCount==7:
                    targetRoad=self.targetRoadList[-3]
                elif loopCount==8:
                    targetRoad=self.startRoad
                elif loopCount==9:
                    self.log.critical("exit: could not find target in daytrip {0}, startRoad: {1}, current road: {3} targetRoad {2} , radius {3}".format(self.unique_id, self.startRoad, targetRoad, self.road, self.radius))
                    exit()
                access=self.roadAccessibility(targetRoad)
                self.log.debug('count of while loop in search target {}'.format(loopCount))
            self.findMyWay(targetRoad)
            self.road=targetRoad
            self.tripCount+=1
            self.log.info("agent {0}, trip count: {1}, trip avg: {2}, number of trips: {3}".format(self.unique_id, self.tripCount, self.agentTravelAvg, self.agentTravelTrip))
        self.log.debug('reset agent  {0}, trip should {1}, trip count {2}'.format(self.unique_id,self.agentTravelTrip,self.tripCount))
        #go back to starting road targetRoad=startRoad
        targetRoad=self.resetAgent()
        self.findMyWay(targetRoad)
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
            self.startRoad=self.findStartLocation()
            self.road=self.startRoad
            self.daytrips()
            #update unique crimes
            self.uniqueCrimesOverall()
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
    
