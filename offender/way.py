#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mesa
from mesa.time import RandomActivation
import Model
import networkx as nx
import numpy as np
import math
import collections
from collections import OrderedDict
import sys, psycopg2, os, time, random, logging
from operator import itemgetter
import globalVar


class Way:
    """agent path options"""
    def __init__(self, unique_id, model, road):
        self.log=logging.getLogger('')
        self.t=time.monotonic()
        self.unique_id=unique_id
        self.model=model
        self.wayfindingType=model.wayfindingType
        self.road=road
        self.targetroad=0
        self.way=[]

    def waybytype(self, targetroad):
        #test
        #nodes for self.road
        #self.road=16123
        #targetroad=12195
        self.targetroad=targetroad
        roadNode=random.choice(list(self.model.roads[self.road]))
        targetNode=random.choice(list(self.model.roads[ self.targetroad]))
        if roadNode==targetNode:
            self.way=[self.road, self.targetroad]
        else:
            getattr(self, self.wayfindingType)(roadNode, targetNode)
        return self.way

    def wayComplete(self, wayN):
        i=0
        way=list()
        while i<len(wayN)-1:
            rl1=set(self.model.intersect[wayN[i]])
            rl2=set(self.model.intersect[wayN[i+1]])
            r=rl1.intersection(rl2)
            #self.road needs to be first road
            way.append(list(r)[0])
            i+=1
        #print("print roads in self.way {}".format(self.way))
        count=0
        #fix beginning and end of self.way
        l=len(way)
        l=len(way)
        r0=list()
        for r in way[:3]:
            r0.append(r)
        rn=list()
        #print(way[-3:])
        for r in way[-3:]:
            #print(r)
            rn.append(r)
        rn.reverse()

        #START: self road is within 3 first roads, remove rest
        #print( self.road, r0)
        if self.road in r0:
            for r in r0:
                if r==self.road:
                    break
                else:
                    #print("remove start {}".format(r))
                    way.remove(r)
        else:
            #print("else")
            way1=nx.shortest_path(self.model.G,self.road,r0[0])
            #will give start and end road if they are the only ones in path

            way1.pop()
            way=way1+way
        #print(way)
        #print("end")
        #print( self.targetroad, rn)
        if  self.targetroad in rn:
            for r in rn:
                #print("for")
                #print(r,  self.targetroad)
                if r== self.targetroad:
                    #print("f: if")
                    break
                else:
                    #print("f: else")
                    #print("remove end {}".format(r))
                    way.remove(r)
        else:
            #print("else")
            #print(rn)
            way2=nx.shortest_path(self.model.G,rn[0],  self.targetroad)
            #print(way2)
            #print("del first duplicate {}".format(way2[0]))
            del way2[0]
            #print(way2)
            way=way+way2
            #print(way)
        return way

    def oldWaynetwork(self, roadNode, targetNode):
            #nodes for self.road
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode)
            way1=self.wayComplete(wayN)
            print("way normal {}".format(way1))
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode, weight='length')
            self.way=self.wayComplete(wayN)
            #print("way length {}".format(self.way))


    def wayLength(self, roadNode, targetNode):

        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode, weight='length')
            self.way=self.wayComplete(wayN)
            #print("way length {}".format(self.way))
        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id, self.targetroad, self.road, self.model.modelStepCount))
            exit()

    def wayWidth(self, roadNode, targetNode):
        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode, weight='width')
            self.way=self.wayComplete(wayN)
            #print("way width {}".format(self.way))
        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id,  self.targetroad, self.road, self.model.modelStepCount))
            exit()

    def wayLengthWidth(self, roadNode, targetNode):
        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode, weight='lengthwidth')
            #print("way length {}".format(wayN))
            self.way=self.wayComplete(wayN)
            #print("way lengthwidth {}".format(self.way))
        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id,  self.targetroad, self.road, self.model.modelStepCount))
            exit()

    def wayRoadtype(self, roadNode, targetNode):
        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode, weight='roadtypelength')
            #print("way length {}".format(wayN))
            self.way=self.wayComplete(wayN)
            #print("way roadtypelength {}".format(self.way))
        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id,  self.targetroad, self.road, self.model.modelStepCount))
            exit()