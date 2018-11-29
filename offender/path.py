#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mesa
from mesa.time import RandomActivation
import Model
from way import Way
import networkx as nx
import numpy as np
import math
from collections import OrderedDict
import sys, psycopg2, os, time, random, logging
from operator import itemgetter
import globalVar


class Path:
    """agent path options"""
    def __init__(self, unique_id, model, currentRoad, distanceType, targetType, tripcount):
        self.log=logging.getLogger('')
        self.conn=model.conn
        self.model=model

        self.unique_id=unique_id

        self.pos=0
        self.foundnoway=0
        self.walkedDistance=1 #distance walked in total
        #TODO create array with initial position and all targets?
        self.walkedRoads=0 
        self.pathroadlist=list()
        self.pathlengtdict=OrderedDict()
        #arrays don't grow efficiently, first build list of tuples and the convert to array!!
        self.pathroadtuple=list()
        self.tripcount=tripcount

        self.crimes=[]
        for i in range(6):
            self.crimes.append([])
     
        ##select starting position by type
        self.road=currentRoad

        self.distanceType=distanceType
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

        self.radius()
        #selection behavior for target type
        self.targetType=targetType
        self.destinationcensus=0
        self.radiusR=0




    def radius(self):
        return(getattr(self, self.distanceType)())

    def staticR(self):
        self.log.info("static radius Agent")
        self.radiusR=self.staticRadius

    def uniformR(self):
        #minimal distance from 2.5km to foot
        self.radiusR=np.random.uniform(self.pmin, self.pmax)
        #self.log.info("uniform radius Agent: {}".format(radius))

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
        self.radiusR=round(radius)


    def taxiTract(self):
        #first find tract for current road (pickup census tract)
        #test
        #TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        censustract=nx.get_node_attributes(self.model.G, 'census').get(self.road)
        try:
            dropoffoptions=self.model.taxiTracts[censustract]
            #print(dropoffoptions)
        except:
            #if census tract not found then random? or most popular? or what??
            print("census tract: {} not found as key in taxiTracts dictionary".format(censustract))
            exit()
        #choose destination census tract (drop off census tract by weight)
        #TODO get pweight from table
        census =list()
        weight =list()
        pWeightList=list()
        for k,v in dropoffoptions.items():
            census.append(k)
            weight.append(int(v))
        weightSum=sum(weight)
        for v in weight:
            pWeightList.append(v/weightSum)
        #print(sum(pWeightList))
        self.destinationcensus=self.selectCensuswithWeight(census, pWeightList)
        #print(self.destinationcensus)

    def taxiTractD(self):
        #first find tract for current road (pickup census tract)
        censustract=nx.get_node_attributes(self.model.G, 'census').get(self.road)
        try:
            dropoffoptions=self.model.taxiTracts[censustract]
            #print(dropoffoptions)
            distanceCT=self.model.distanceCT[censustract]
        except:
            #if census tract not found then random? or most popular? or what??
            print("census tract: {} not found as key in taxiTracts dictionary".format(censustract))
            exit()
        #choose destination census tract (drop off census tract by weight)
        #TODO get pweight from table
        #taxi data
        tcensus =list()
        tweight =list()
        #census tract distance data
        dweight =list()
        for k,v in dropoffoptions.items():
            tcensus.append(k)
            #weight from taxi data
            tweight.append(int(v))
            #distance for same census tract
            dweight.append(distanceCT[k])
        pWeightList=self.combine2weights(tweight, dweight)
        self.destinationcensus=self.selectCensuswithWeight(tcensus, pWeightList)

    def crimeTractM(self):
        """data for may2015"""
        crimeCT=self.model.crimeCT
        p=list([item[0] for item in crimeCT.values()])
        destinationcensus=np.random.choice(list(crimeCT.keys()), 1, p=p)[0]
        self.destinationcensus=destinationcensus
        return destinationcensus 
    def crimeTractMD(self):
        """data for may2015 weighted by census tract distance"""
        #distance from current CT to others
        censustract=nx.get_node_attributes(self.model.G, 'census').get(self.road)
        distanceCT=self.model.distanceCT[censustract]
        #probabilities for CT by crime
        crimeCT=self.model.crimeCT
        census=list(crimeCT.keys())
        p=list([item[0] for item in crimeCT.values()])
        dcensus=list()
        #distance weight in same order as census and p
        for c in census:
            dcensus.append(distanceCT[c])
        pWeightList=self.combine2weights(p, dcensus)
        self.destinationcensus=self.selectCensuswithWeight(census, pWeightList) 
    def crimeTract1(self):
        """data for june14-may15"""
        crimeCT=self.model.crimeCT
        p=list([item[1] for item in crimeCT.values()])
        destinationcensus=np.random.choice(list(crimeCT.keys()), 1, p=p)[0]
        self.destinationcensus=destinationcensus
    def crimeTract1x2(self):
        """data for june14-may15*2"""
        crimeCT=self.model.crimeCT
        p=list([item[2] for item in crimeCT.values()])
        destinationcensus=np.random.choice(list(crimeCT.keys()), 1, p=p)[0]
        self.destinationcensus=destinationcensus
    def crimeTract1x6(self):
        """data for june14-may15*6"""
        crimeCT=self.model.crimeCT
        p=list([item[3] for item in crimeCT.values()])
        destinationcensus=np.random.choice(list(crimeCT.keys()), 1, p=p)[0]
        self.destinationcensus=destinationcensus
    def crimeTract1x12(self):
        """june14-may15*12"""
        crimeCT=self.model.crimeCT
        p=list([item[4] for item in crimeCT.values()])
        destinationcensus=np.random.choice(list(crimeCT.keys()), 1, p=p)[0]
        self.destinationcensus=destinationcensus
    def crimeTract1x12D(self):
        """june14-may15*12 weighted by census tract distance"""
        #distance from current CT to others
        censustract=nx.get_node_attributes(self.model.G, 'census').get(self.road)
        distanceCT=self.model.distanceCT[censustract]
        #probabilities for CT by crime
        crimeCT=self.model.crimeCT
        census=list(crimeCT.keys())
        p=list([item[4] for item in crimeCT.values()])
        dcensus=list()
        #distance weight in same order as census and p
        for c in census:
            dcensus.append(distanceCT[c])
        pWeightList=self.combine2weights(p, dcensus)
        self.destinationcensus=self.selectCensuswithWeight(census, pWeightList)
    
    def selectCensuswithWeight(self, censusList, pWeightList):
        try:
            destinationcensus=np.random.choice(censusList, 1, p=pWeightList)[0]
            #print(destinationcensus)
        except:
            #correct weights if it list does not sum up to 1
            spweight=sum(pWeightList)
            if (spweight)!= 1:
                val=min(pWeightList)
                idx=pWeightList.index(val)
                rest=1-spweight
                pWeightList[idx]=val+rest
            destinationcensus=np.random.choice(censusList, 1, p=pWeightList)[0]
        return destinationcensus


    def combine2weights(self, weight1, weight2):
        combineW=list()
        pWeightList=list()
        weight1Sum=sum(weight1)
        weight2Sum=sum(weight2)
        if not len(weight1)==len(weight2):
            self.log.critical("in path weight1 and teight2 do not have same length")
        i=0
        while i<len(weight1):
            combineW.append((weight1[i]/weight1Sum)*(weight2[i]/weight2Sum))
            i+=1
        combineWSum=sum(combineW)
        i=0
        while i<len(weight1):
            pWeightList.append(combineW[i]/combineWSum)
            i+=1
        #print(sum(pWeightList))
        return pWeightList

    def findTargetByType(self, road, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        return(getattr(self, self.model.targetType)(road, mycurs, maxRadius, minRadius))

    def randomRoad(self, road, mycurs, maxRadius, minRadius):
        if 'Tract' in self.distanceType:
            mycurs.execute("""select gid from (select r.gid, s.new_gid,  s.new_gid_ftus
                from open.nyc_road_proj_final as r, open.nyc_road2censustract s
                where s.new_gid={0} and st_intersects(r.geom,s.new_gid_ftus) and
                r.gid not in (select * from open.nyc_road_proj_final_isolates)) as bar""".format(self.destinationcensus))
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
        if 'Tract' in self.distanceType:
            mycurs.execute("""select gid, weight_center from (select r.gid, r.weight_center, s.new_gid,  s.new_gid_ftus
                from open.nyc_road_weight_to_center as r, open.nyc_road2censustract s
                where s.new_gid={0} and st_intersects(r.geom,s.new_gid_ftus) and
                r.gid not in (select * from open.nyc_road_proj_final_isolates)) as bar""".format(self.destinationcensus))
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
        if 'Tract' in self.distanceType:
            mycurs.execute("""select road_id from (select venue_id, road_id, r2c.new_gid,  r2c.new_gid_ftus
                     from open.nyc_fs_venue_join fs
                     left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                     left join open.nyc_road2censustract r2c on r2c.gid=r2f.road_id
                     where r2c.new_gid={0} and st_intersects(fs.ftus_coord,r2c.new_gid_ftus)
                     and not r2f.road_id is null and road_id not in
                     (select gid from open.nyc_road_proj_final_isolates)) as bar""".format(self.destinationcensus))
        elif maxRadius == 41000:
            """mapping results slightly different - because query roads within radius not venues like this"""
            mycurs.execute("""select road_id from (select venue_id, startroad, targetroad, road_id from open.nyc_fs_venue_join as v
               left join open.nyc_road2fs_near2 r2f on r2f.fs_id=v.venue_id 
               left join open.nyc_road2road_precalc r on r.targetroad=r2f.road_id) as f where startroad={0}
               and road_id not in (select * from open.nyc_road_proj_final_isolates)""".format(road))
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
        if 'Tract' in self.distanceType:
            mycurs.execute("""select road_id, weight_center from (select venue_id, road_id, weight_center
                from open.nyc_fs_venue_join_weight_to_center fs
                left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                left join open.nyc_road2censustract r2c on r2c.gid=r2f.road_id
                where r2c.new_gid={} and st_intersects(fs.ftus_coord,r2c.new_gid_ftus)
                and not r2f.road_id is null and road_id not in
                (select gid from open.nyc_road_proj_final_isolates)) as bar""".format(self.destinationcensus))
        elif maxRadius == 41000:
            """mapping results slightly different - because query roads within radius not venues like this"""
            mycurs.execute("""select road_id, weight_center from (
                select venue_id,road_id, weight_center, startroad, targetroad from open.nyc_fs_venue_join_weight_to_center as fs
    			left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
    			left join open.nyc_road2road_precalc r on r.targetroad=r2f.road_id) as f where startroad={0}
                and not road_id is null and not weight_center=0
                and road_id not in (select * from open.nyc_road_proj_final_isolates)""".format(road))
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

    def randomVenueType(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        if 'Tract' in self.distanceType:
            mycurs.execute("""select road_id, parent_name from (select venue_id, road_id, r2c.new_gid,  r2c.new_gid_ftus, parent_name
                     from open.nyc_fs_venue_join fs
                     left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                     left join open.nyc_road2censustract r2c on r2c.gid=r2f.road_id
                     where r2c.new_gid={0} and st_intersects(fs.ftus_coord,r2c.new_gid_ftus)
                     and not r2f.road_id is null and road_id not in
                     (select gid from open.nyc_road_proj_final_isolates)) as bar""".format(self.destinationcensus))
        elif maxRadius == 41000:
            """mapping results slightly different - because query roads within radius not venues like this"""
            mycurs.execute("""select road_id, parent_name from (select venue_id, startroad, targetroad, road_id, parent_name
               from open.nyc_fs_venue_join as v
               left join open.nyc_road2fs_near2 r2f on r2f.fs_id=v.venue_id 
               left join open.nyc_road2road_precalc r on r.targetroad=r2f.road_id) as f where startroad={0}
               and road_id not in (select * from open.nyc_road_proj_final_isolates)""".format(road))
        else:
            mycurs.execute("""select road_id, parent_name from (
                select venue_id, parent_name from open.nyc_fs_venue_join where st_dwithin( (
                select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {1})
                and not st_dwithin( (
                select geom from open.nyc_road_proj_final where gid={0}) ,ftus_coord, {2}))
                as fs left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                where not road_id is null
                and road_id not in (select * from open.nyc_road_proj_final_isolates)""".format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple of tuples, venue_id and road_id paired
        self.log.debug('random Venue')        
        return roads  

    def popularVenue(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        if 'Tract' in self.distanceType:
            mycurs.execute("""select road_id, checkins_count from (select venue_id, road_id, checkins_count
                from open.nyc_fs_venue_join fs
                left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                left join open.nyc_road2censustract r2c on r2c.gid=r2f.road_id
                where r2c.new_gid={} and st_intersects(fs.ftus_coord,r2c.new_gid_ftus)
                and not r2f.road_id is null and road_id not in
                (select gid from open.nyc_road_proj_final_isolates)) as bar""".format(self.destinationcensus))
        elif maxRadius == 41000:
            """mapping results slightly different - because query roads within radius not venues like this"""
            mycurs.execute("""SELECT road_id, checkins_count FROM(
                SELECT venue_id, checkins_count, startroad, targetroad, road_id from open.nyc_fs_venue_join as fs
                LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id
                LEFT JOIN open.nyc_road2road_precalc r on r.targetroad=r2f.road_id) as f where startroad={0}
                and NOT road_id is null and road_id not in (select * from open.nyc_road_proj_final_isolates)""".format(road))
        else:
            mycurs.execute("""SELECT road_id, checkins_count FROM(
                SELECT venue_id, checkins_count
                from open.nyc_fs_venue_join
                where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
                and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2}))
                AS fs LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id WHERE NOT road_id is null
                and road_id not in (select * from open.nyc_road_proj_final_isolates)"""
                .format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple of tuples, venue_id,weighted_checkins
        self.log.debug('popular Venue') 
        return roads

    def popularVenueCenter(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        #venues venue_id=270363 or venue_id=300810 are incorrectly mapped and therefore have weihgt=0, should not be accoutned for
        if 'Tract' in self.distanceType:
            mycurs.execute("""select road_id, weight_center, checkins_count from (
    			select venue_id, road_id, checkins_count, weight_center
                from open.nyc_fs_venue_join_weight_to_center fs
                left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                left join open.nyc_road2censustract r2c on r2c.gid=r2f.road_id
                where r2c.new_gid={} and st_intersects(fs.ftus_coord,r2c.new_gid_ftus)
                and not r2f.road_id is null and road_id not in
                (select gid from open.nyc_road_proj_final_isolates)) as bar""".format(self.destinationcensus))
        elif maxRadius == 41000:
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
    
    def popularVenueType(self, road, mycurs, maxRadius, minRadius):
        mycurs = self.conn.cursor()
        if 'Tract' in self.distanceType:
            mycurs.execute("""select road_id, checkins_count, parent_name from (select venue_id, road_id, checkins_count, parent_name
                from open.nyc_fs_venue_join fs
                left join open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id 
                left join open.nyc_road2censustract r2c on r2c.gid=r2f.road_id
                where r2c.new_gid={} and st_intersects(fs.ftus_coord,r2c.new_gid_ftus)
                and not r2f.road_id is null and road_id not in
                (select gid from open.nyc_road_proj_final_isolates)) as bar""".format(self.destinationcensus))
        elif maxRadius == 41000:
            """mapping results slightly different - because query roads within radius not venues like this"""
            mycurs.execute("""SELECT road_id, checkins_count, parent_name FROM(
                SELECT venue_id, checkins_count, startroad, targetroad, road_id, parent_name from open.nyc_fs_venue_join as fs
                LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id
                LEFT JOIN open.nyc_road2road_precalc r on r.targetroad=r2f.road_id) as f where startroad={0}
                and NOT road_id is null and road_id not in (select * from open.nyc_road_proj_final_isolates)""".format(road))
        else:
            mycurs.execute("""SELECT road_id, checkins_count, parent_name FROM(
                SELECT venue_id, checkins_count, parent_name
                from open.nyc_fs_venue_join
                where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
                and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2}))
                AS fs LEFT JOIN open.nyc_road2fs_near2 r2f on r2f.fs_id=fs.venue_id WHERE NOT road_id is null
                and road_id not in (select * from open.nyc_road_proj_final_isolates)"""
                .format(road,maxRadius,minRadius))
        roads=mycurs.fetchall() #returns tuple of tuples, road_id, checkins, venueType
        self.log.debug('popular Venue Type') 
        return roads

    


    def searchTarget(self, road):
        """search target within radius"""
        #print('in searchTarget: current road for new target: {0}'.format(road))
        targetRoad=0
        count=0
        roadId=None
        #5% boundry ~0.6 km
        maxRadius=self.radiusR*1.025
        #in repast it was set to 0.925 - error
        minRadius=self.radiusR*0.975
        while targetRoad==0:
            count+=1
            roads=self.findTargetByType(road, maxRadius, minRadius)
            roadId=self.weightedChoice(roads, road)
            if not roadId is None:
                targetRoad=roadId
                return (targetRoad)
            #enlarge by 10%
            maxRadius=maxRadius*1.05
            minRadius=minRadius*0.95
            if count>1 and count<=5:
                self.radius()
                maxRadius=self.radiusR*1.025
                minRadius=self.radiusR*0.975
                #self.log.debug('new radius: {}'.format(self.radius))
            if count>5:
                self.radius()
                maxRadius=self.radiusR*1.025
                minRadius=self.radiusR*0.975
                #self.log.debug('new radius: {}'.format(self.radius))
            elif count>10:
                self.log.critical("**********5 radius didn't work: agent id {0}, current road: {1} targetRoad {2} , radius {3}".format(self.unique_id, targetRoad, self.road, self.radiusR))
        return targetRoad

    def weightedChoice(self, roads, road):
        """choice of target by weighting if avalable"""
        #TODO bring weihts to same scale!!!
        if not roads:
            self.log.debug('no roads in radius, road {0}, search radius: {1}, distanceType: {2}'.format(road, self.radiusR, self.distanceType))
            roadId=None   
        elif (len(roads[0]) is 1):
            road=random.choice(roads)
            roadId=road[0]
        elif 'Type' in str(self.targetType):
            #line0: roads, line[1]: checkins, line[2]:parent_name or venue type
            roadsList=[x[0] for x in roads]           
            if (len(roads[0])>2): #×or if self.targetType=2
                weightList=[x[1] for x in roads]
                venueType=[x[2] for x in roads]
                weightListT=list()
                for v in venueType:
                    vtw=self.model.venueTypeweight[v]
                    weightListT.append(vtw)
                weightList=[i*j for i,j in zip(weightList,weightListT)]
                self.log.debug('combined weights: {}'.format(weightList[0]))
            else:
                venueType=[x[1] for x in roads]
                weightList=list()
                for v in venueType:
                    vtw=self.model.venueTypeweight[v]
                    weightList.append(vtw)
                self.log.debug('weights: {}'.format(weightList[0]))
            pWeightList=[]
            sumWeightList=sum(weightList)
            for value in weightList:
                pWeightList.append(value/sumWeightList)
            self.log.debug('weightlist p sum: {}'.format(sum(pWeightList)))
            roadIdNp=np.random.choice(roadsList, 1, True, pWeightList)
            roadId=roadIdNp[0]  
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
            attributList=self.model.allCrimes[road]
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


    def findMyWay(self, targetroad):
        """find way to target road and count statistics for path"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        #print(self.road, targetroad)
        roadValuesList=[]
        if self.road==targetroad:
            self.way=[targetroad]
            self.log.debug("road and target road are the same")
        else:
            try:
                w=Way(self.unique_id, self.model, self.road)
                self.way=w.waybytype(targetroad)

                ###QRunner seems not to be working --  or may be taking too long?? take out for calculating 1000 agents
                #self.model.insertQ.store_roads({"run_id": self.model.run_id, "step": self.model.modelStepCount,
                #          "agent": self.unique_id, "way": self.way})
                i=0
                for road in self.way:
                    #print("for road: {}".format(road))
                    #print(self.model.G.node[road]['length'])
                    self.walkedDistance += self.model.G.node[road]['length']
                    #print("crimes")
                    self.crimesOnRoad(road)
                    #print("walked")
                    self.walkedRoads +=1
                    ##has to be commented if want to use Qrunner
                    sql = """insert into abm_res.res_la_roadsprototype ("id","run_id","step","agent","road_id", i, trip) values
                        (DEFAULT,{0},{1},{2},{3},{4},{5})""".format(self.model.run_id, self.model.modelStepCount, self.unique_id, road, i, self.tripcount)
                    self.model.mycurs.execute(sql)
                    #print("execute")
                    self.pathroadlist.append(road)
                    #print("pathroadlist")
                    i+=1
                self.model.conn.commit()
            except Exception as e:
                self.log.critical("trip: Error: One agent found no way: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id, targetroad, self.road, self.model.modelStepCount))
                exit()
            #erases target from targetList
        return True   


    def roadAccessibility(self):
        """test if there is a way to the road"""
        try:
            self.way=nx.shortest_path(self.model.G,7,self.targetRoad)
            return True
        except:
            return False

    def buildpathhome(self, homeRoad):
        #print("path back home")
        loopCount=0
        access=False
        while access==False:
            loopCount+=1
            if loopCount==8:
                self.log.critical("exit: could not find target current road: {0} targetRoad {1} , radius {2}".format(self.road, homeRoad, self.radiusR))
            access=self.findMyWay(homeRoad)
            #self.log.debug('count of while loop in search target {}'.format(loopCount))
        self.uniqueCrimesOverall()
        #return self.pathroadlist
        return homeRoad

    def buildpath(self):
        #print("path anywhere")
        self.radius()
        #agent trip number drawn form distribution
        loopCount=0
        #emulate do-while: assigns False for the loop to be executed before further condition testing
        access=False
        while access==False:
            loopCount+=1
            targetRoad=self.searchTarget(self.road)
            if targetRoad in globalVar.isolateRoadsRNW:
                access=False
                continue
            if loopCount==8:
                self.log.critical("exit: could not find target current road: {0} targetRoad {1} , radius {2}".format(self.road, targetRoad, self.radiusR))
            access=self.findMyWay(targetRoad)
            #self.log.debug('count of while loop in search target {}'.format(loopCount))
        self.uniqueCrimesOverall()
        #return self.pathroadlist
        return targetRoad