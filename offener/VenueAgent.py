import mesa
from mesa.time import RandomActivation
import Model
import networkx as nx
import numpy as np
import math
import sys, psycopg2, os, time, random, logging

class VenueAgent(mesa.Agent):
    """an Agent moving"""
    def __init__(self, unique_id, model, radiusType):
        super().__init__(unique_id, model)
        self.pos=0
        self.startRoad=self.findStartLocation(model)
        print("startRoad: {0}".format(self.startRoad))
        self.road=self.startRoad
        self.conn=model.conn

        #list of positions offender has visited
        self.targetRoadList=[self.startRoad]

        #select starting position by type

        #selection behavior for radius type
        #static
        if radiusType is 0 :
            self.searchRadius=model.staticRadius
            print('static radius Agent')
        #uniform
        elif radiusType is 1 :
            self.searchRadius=model.uniformRadius
            print('uniform radius Agent')
        #power
        elif radiusType is 2 :
            self.mu=model.mu
            self.dmin=model.dmin
            self.dmax=model.dmax
            self.searchRadius=self.powerRadius(self.mu, self.dmin, self.dmax)
            print('power radius Agent is {0}'.format(self.searchRadius))
        self.radiusType=radiusType

        

        #statistics
        self.seenCrimes=0 #historic crimes passed on path
        self.walkedDistance=0 #distance walked in total
        #TODO create array with initial position and all targets?
        self.walkedRoads=0 
        
        self.log=logging.getLogger('')
        
        #find new target    
        self.targetRoad=self.searchTarget(self.road, self.searchRadius)
        self.findMyWay()

    def findStartLocation(self, model):
        #select startingPoint from random sample of nodes
        return random.sample(model.G.nodes(),1)[0]

    def searchTarget(self, road, searchRadius):
        if road is None:
            road=self.startRoad
        print('searchTarget current road for new target: {0}'.format(road))
        mycurs = self.conn.cursor()
        targetRoad=0

        maxRadius=searchRadius*1.025
        #in repast it was set to 0.925 - error
        minRadius=searchRadius*0.975

        #TODO query does not output random roads!
        #TODO get all the venues within distance
        count=0
        targetRoad=0
        while targetRoad==0:
            count+=1
            print('search target road iteration {}'.format(count))
            mycurs.execute("""select st_astext(geom) from open.nyc_road_proj_final where gid={}""".format(self.road))
            roadLocation=mycurs.fetchall()[0][0]
            mycurs.execute("""select gid from (
                select gid,geom from open.nyc_road_proj_final where st_dwithin(
                (select geom from open.nyc_road_proj_final where gid={0}),geom,{1})
                and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}) ,geom,{2})
                ) as bar;""".format(roadLocation,maxRadius,minRadius))
            roadId=mycurs.fetchone() #returns tuple with first row (unordered list)
            if not roadId is None:
                targetRoad=roadId[0]
                #print("roadid in target: {0}".format(roadId[0]))
                self.targetRoadList.append(targetRoad)
                return (targetRoad)
            searchRadius=searchRadius/10 #enlargen radius by 10%
            return targetRoad
        
    def findMyWay(self):
        try:
            #roads are represented as nodes in G
            self.way=nx.shortest_path(self.model.G,self.road,self.targetRoad,weight='length')
            #print("Agent ({0}) way: {1}".format(self.unique_id,self.way))
        except Exception as e:
            print ("Error: One agent found no way: ",e,self.unique_id)
            self.way=[self.road,self.targetRoad]

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
        #select new radius for power-law
        if self.radiusType is 2:
            self.searchRadius=self.powerRadius(self.mu, self.dmin, self.dmax)
            print('next power radius {0}'.format(self.radiusType))
        #one step: walk to destination
        for road in self.way:
            self.walkedDistance += self.model.G.node[road]['length']
            self.seenCrimes += self.model.G.node[road]['num_crimes']
            #print("Agent at distance: {0}".format(self.unique_id))
            #print("Agent {0}, seen {1} crimes, traveled {2}".format(
            #self.unique_id,self.seenCrimes,self.walkedDistance))
        road=self.targetRoad
        #find new target
        self.targetRoad=self.searchTarget(road, self.searchRadius)
        self.findMyWay()
        print('agent {0}, target road list by road_id {1}'.format(self.unique_id, self.targetRoadList))
        print('step done for agent {0}'.format(self.unique_id))      

        