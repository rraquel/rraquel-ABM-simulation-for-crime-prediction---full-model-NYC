import mesa
from mesa.time import RandomActivation
import networkx as nx
import sys, psycopg2, os, time, random, logging

class Agent(mesa.Agent):
    """an Agent moving"""
    def __init__(self, unique_id, model, startRoad, targetRoad):
        super().__init__(unique_id, model)
        self.pos=0
        self.road=startRoad
        self.targetRoad=targetRoad

        #statistics
        self.seenCrimes=0 #historic crimes passed on path
        self.walkedDistance=0 #distance walked in total
        self.walkedRoads=0 

        self.log=logging.getLogger('')

        self.findMyWay()

    def findMyWay(self):
        try:
            #roads are represented as nodes in G
            self.way=nx.shortest_path(self.model.G,self.road,self.targetRoad,weight='length')
            print("Agent ({0}) way: {1}".format(self.unique_id,self.way))
        except Exception as e:
            print ("Error: One agent found no was: ",e,self.unique_id)
            self.way=[self.road,self.targetRoad]

    def step(self):
        """step: behavior for each offender"""
        #one step: walk to destination
        for road in self.way:
            self.walkedDistance += self.model.G.node[road]['length']
            self.seenCrimes += self.model.G.node[road]['num_crimes']
        print("Agent at distance: {}".format(self.unique_id))
        print("Agent {0}, seen {1} crimes, traveled {2}".format(
            self.unique_id,self.seenCrimes,self.walkedDistance))
        #find new target
        self.targetRoad=self.model.findTargetLocation(road)
        self.findMyWay()
        print('step done for agent ')
        