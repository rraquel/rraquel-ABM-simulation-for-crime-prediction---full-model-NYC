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
import globalVar


class AgentX(mesa.Agent):
    """an Agent moving"""
    def __init__(self, unique_id, model, radiusType, targetType, startLocationType, agentTravelAvg):
        super().__init__(unique_id, model)
        self.log=logging.getLogger('')
        self.unique_id=unique_id
        self.model=model
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
        self.startRoad=findStartLocation(self.model, self.startLocationType, self.unique_id)
        self.road=self.startRoad

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
        self.destinationCensus=None
        self.searchRadius=0


        if 'taxiTract' in self.radiusType:
            self.destinationCensus=self.taxiTract()
        else:
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


    def resetAgent(self):
        self.tripCount=0
        self.targetRoadList.append(self.startRoad)
        self.log.debug("reset agent")
        #TODO if agent starts at new position, need to find new start location!!!
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

    def taxiTract(self):
        #first find tract for current road (pickup census tract)
        #test
        #TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        road=7
        print(road)
        censustract=nx.get_node_attributes(self.model.G, 'census').get(road)
        dropoffoptions=self.model.taxiTracts[censustract]
        #choose destination census tract (drop off census tract by weight)
        dcensus =list()
        dweight =list()
        pWeightList=list()
        print(type(dropoffoptions.items()))
        for k,v in dropoffoptions.items():
            dcensus.append(k)
            dweight.append(v)
        weightSum=sum(dweight)
        for v in dweight:
            pWeightList.append(v/weightSum)
        print(np.random.choice(dcensus, 1, p=pWeightList))
        destinationcensus=np.random.choice(dcensus, 1, p=pWeightList)[0]
        return destinationcensus

    def findTargetByType(self, road, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        return(getattr(self, self.model.targetType)(road, mycurs, maxRadius, minRadius))

    def randomRoad(self, road, mycurs, maxRadius, minRadius):
        if 'taxiTract' in self.radiusType:
            mycurs.execute("""select gid from (select r.gid, s.new_gid,  s.new_gid_ftus
                from open.nyc_road_proj_final as r, open.nyc_road2censustract s
                where s.new_gid={0} and st_intersects(r.geom,s.new_gid_ftus) and
                r.gid not in (select * from open.nyc_road_proj_final_isolates)) as bar""").format(self.destinationCensus)
        elif maxRadius == 41000:
            mycurs.execute("""select targetroad as gid from open.nyc_road2road_precalc where startroad={0} and radius=40000 and 
                model='road' and targetroad not in (select * from open.nyc_road_proj_final_isolates)""".format(road))
        else:
            # If something goes really wrong, we use old techniques (change min and max)
            mycurs.execute("""select gid from (
                select gid,geom from open.nyc_road_weight_to_center where st_dwithin(
                (select geom from open.nyc_road_weight_to_center where gid={0}),geom,{1})
                and not st_dwithin((select geom from open.nyc_road_weight_to_center where gid={0}) ,geom,{2})
                and gid not in (select * from open.nyc_road_proj_final_isolates)
                ) as bar;""".format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple with first row (unordered list)
        self.log.debug('random Road')
        return roads

    def randomRoadCenter(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        if 'taxiTract' in self.radiusType:
            mycurs.execute("""select gid, weight_center from (select r.gid, r.weight_center, s.new_gid,  s.new_gid_ftus
                from open.nyc_road_weight_to_center as r, open.nyc_road2censustract s
                where s.new_gid={0} and st_intersects(r.geom,s.new_gid_ftus) and
                r.gid not in (select * from open.nyc_road_proj_final_isolates)) as bar""").format(self.destinationCensus)
        elif maxRadius == 41000:
            mycurs.execute("""select gid,weight_center from (select gid, weight_center, startroad, targetroad from open.nyc_road_weight_to_center as r
               left join open.nyc_road2road_precalc as c on c.targetroad=r.gid) as f where startroad={0}
               and gid not in (select * from open.nyc_road_proj_final_isolates);""".format(road))
        else:
            mycurs.execute("""select gid,weight_center from (
                select gid,weight_center,geom from open.nyc_road_weight_to_center where st_dwithin(
                (select geom from open.nyc_road_weight_to_center where gid={0}),geom,{1})
                and not st_dwithin((select geom from open.nyc_road_weight_to_center where gid={0}) ,geom,{2})
                and gid not in (select * from open.nyc_road_proj_final_isolates)
                ) as bar;""".format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple with first row (unordered list)
        #self.log.debug('random Road Center')
        return roads

    def randomVenue(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        if maxRadius == 41000:
            """mapping results slightly different - because query roads within radius not venues like this"""
            mycurs.execute("""select road_id from (select venue_id, startroad, targetroad, road_id from open.nyc_fs_venue_join as v
               left join open.nyc_road2fs_near2 r2f on r2f.fs_id=v.venue_id 
               left join open.nyc_road2road_precalc r on r.targetroad=r2f.road_id) as f where startroad={0}
               and road_id not in (select * from open.nyc_road_proj_final_isolates);""".format(road))
        else:
            mycurs.execute("""select road_id from (
                select venue_id from open.nyc_fs_venue_join where st_dwithin( (
                select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {1})
                and not st_dwithin( (
                select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {2}))
                as fs left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                where not road_id is null
                and road_id not in (select * from open.nyc_road_proj_final_isolates)""".format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple of tuples, venue_id and road_id paired
        self.log.debug('random Venue')        
        return roads    

    def randomVenueCenter(self, road, mycurs,  maxRadius, minRadius):
        mycurs = self.conn.cursor()
        #venues venue_id=270363 or venue_id=300810 are incorrectly mapped and therefore have weihgt=0, should not be accoutned for
        if maxRadius == 41000:
            """mapping results slightly different - because query roads within radius not venues like this"""
            mycurs.execute("""select road_id, weight_center from (
                select venue_id,road_id, weight_center, startroad, targetroad from open.nyc_fs_venue_join_weight_to_center as fs
    			left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
    			left join open.nyc_road2road_precalc r on r.targetroad=r2f.road_id) as f where startroad={0}
                and not road_id is null and not weight_center=0
                and road_id not in (select * from open.nyc_road_proj_final_isolates);;""".format(road))
        else:
            mycurs.execute("""select road_id, weight_center from (
                select venue_id,weight_center from open.nyc_fs_venue_join_weight_to_center WHERE st_dwithin( (
                select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {1})
                and not st_dwithin( (
                select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {2}))
                as fs left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                where not road_id is null and not weight_center=0
                and road_id not in (select * from open.nyc_road_proj_final_isolates)""".format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple of tuples, venue_id and road_id paired
        #self.log.debug('random Venue Center')        
        return roads

    def popularVenue(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        if maxRadius == 41000:
            """mapping results slightly different - because query roads within radius not venues like this"""
            mycurs.execute("""SELECT road_id, checkins_count FROM(
                SELECT venue_id, checkins_count, startroad, targetroad, road_id from open.nyc_fs_venue_join as fs
                LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id
                LEFT JOIN open.nyc_road2road_precalc r on r.targetroad=r2f.road_id) as f where startroad={0}
                and NOT road_id is null and road_id not in (select * from open.nyc_road_proj_final_isolates);""".format(road))
        else:
            mycurs.execute("""SELECT road_id, checkins_count FROM(
                SELECT venue_id, checkins_count
                from open.nyc_fs_venue_join
                where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
                and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2}))
                AS fs LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id WHERE NOT road_id is null
                and road_id not in (select * from open.nyc_road_proj_final_isolates);"""
                .format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple of tuples, venue_id,weighted_checkins
        self.log.debug('popular Venue') 
        return roads

    def popularVenueCenter(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        #venues venue_id=270363 or venue_id=300810 are incorrectly mapped and therefore have weihgt=0, should not be accoutned for
        if maxRadius == 41000:
            """mapping results slightly different - because query roads within radius not venues like this"""
            mycurs.execute("""SELECT road_id, weight_center, checkins_count FROM(
                SELECT venue_id, weight_center, checkins_count, road_id, startroad, targetroad
    			from open.nyc_fs_venue_join_weight_to_center AS fs
    			LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                left join open.nyc_road2road_precalc r on r.targetroad=r2f.road_id) as f where startroad={0}
    			AND NOT weight_center=0 and NOT road_id is NULL
                and road_id not in (select * from open.nyc_road_proj_final_isolates)""".format(road))
        else:
            mycurs.execute("""SELECT road_id, weight_center, checkins_count FROM(
                SELECT venue_id, weight_center, checkins_count
                from open.nyc_fs_venue_join_weight_to_center
                where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
                and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2}))
                AS fs LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id
                WHERE NOT road_id is NULL AND NOT weight_center=0 and 
                road_id not in (select * from open.nyc_road_proj_final_isolates)"""
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

            ###QRunner seems not to be working --  or may be taking too long?? take out for calculating 1000 agents
            #self.model.insertQ.store_roads({"run_id": self.model.run_id, "step": self.model.modelStepCount,
            #          "agent": self.unique_id, "way": self.way})
            for road in self.way:
                self.walkedDistance += self.model.G.node[road]['length']
                self.crimesOnRoad(road)
                self.walkedRoads +=1

                ##has to be commented if want to use Qrunner
                sql = """insert into open.res_la_roads ("id","run_id","step","agent","road_id") values
                    (DEFAULT,{0},{1},{2},{3} )""".format(self.model.run_id, self.model.modelStepCount, self.unique_id, road)
                self.model.mycurs.execute(sql)

            self.foundnoway=0
        except Exception as e:
            self.log.info("Exception: ", str(e))
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
        if 'taxiTract' not in self.radiusType:
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
            self.startRoad=findStartLocation(self.model, self.startLocationType, self.unique_id)
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
    
