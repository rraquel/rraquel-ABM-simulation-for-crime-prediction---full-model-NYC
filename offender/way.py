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
        self.way=[]

    def waybytype(self, targetroad):
        getattr(self, self.wayfindingType)(targetroad)
        return self.way

    def wayComplete(self, targetroad, wayN):
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
        r0=way[0]
        r1=way[1]
        r2=way[2]
        rn0=way[l-3]
        rn1=way[l-2]
        rn2=way[l-1]
        #START: self road is within 3 first roads, remove rest
        #print(self.road, r0, r1, r2)
        if self.road in {r0, r1, r2}:
            for r in [r0, r1, r2]:
                if r==self.road:
                    break
                else:
                    way.remove(r)
        else:
            #print("else")
            way1=nx.shortest_path(self.model.G,self.road,r0)
            #will give start and end road if they are the only ones in path
            #print(way1)
            way1.pop()
            way=way1+way
        #print(self.way)
        #print("end")
        #print(targetroad, rn2, rn1, rn0)
        if targetroad in {rn2, rn1, rn0}:
            for r in [rn2, rn1, rn0]:
                #print("for")
                #print(r, targetroad)
                if r==targetroad:
                    #print("f: if")
                    break
                else:
                    #print("f: else")
                    way.remove(r)
        else:
            #print("else")
            way2=nx.shortest_path(self.model.G,rn2, targetroad)
            #print(way2)
            way2.remove(rn2)
            way=way+way2
        return way

    def oldWaynetwork(self, targetroad):
            #nodes for self.road
            roadNode=random.choice(list(self.model.roads[self.road]))
            targetNode=random.choice(list(self.model.roads[targetroad]))
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode)
            way1=self.wayComplete(targetroad, wayN)
            print("way normal {}".format(way1))
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode, weight='length')
            self.way=self.wayComplete(targetroad, wayN)
            #print("way length {}".format(self.way))


    def wayLength(self, targetroad):

        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            #test
            #nodes for self.road
            #self.road=16123
            #targetroad=12195
            roadNode=random.choice(list(self.model.roads[self.road]))
            targetNode=random.choice(list(self.model.roads[targetroad]))
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode, weight='length')
            self.way=self.wayComplete(targetroad, wayN)
            #print("way length {}".format(self.way))
        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id, targetroad, self.road, self.model.modelStepCount))
            exit()

    def wayWidth(self, targetroad):
        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            #test
            #nodes for self.road
            #self.road=28729
            #targetroad=81317
            roadNode=random.choice(list(self.model.roads[self.road]))
            targetNode=random.choice(list(self.model.roads[targetroad]))
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode, weight='width')
            self.way=self.wayComplete(targetroad, wayN)
            #print("way width {}".format(self.way))
        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id, targetroad, self.road, self.model.modelStepCount))
            exit()

    def wayLengthWidth(self, targetroad):
        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            #test
            #nodes for self.road
            #self.road=28729
            #targetroad=81317
            roadNode=random.choice(list(self.model.roads[self.road]))
            targetNode=random.choice(list(self.model.roads[targetroad]))
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode, weight='lengthwidth')
            #print("way length {}".format(wayN))
            self.way=self.wayComplete(targetroad, wayN)
            #print("way lengthwidth {}".format(self.way))
        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id, targetroad, self.road, self.model.modelStepCount))
            exit()

    def wayRoadtype(self, targetroad):
        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            #test
            #nodes for self.road
            #self.road=28729
            #targetroad=81317            
            roadNode=random.choice(list(self.model.roads[self.road]))
            targetNode=random.choice(list(self.model.roads[targetroad]))
            wayN=nx.shortest_path(self.model.G2,roadNode,targetNode, weight='roadtypelength')
            #print("way length {}".format(wayN))
            self.way=self.wayComplete(targetroad, wayN)
            #print("way roadtypelength {}".format(self.way))
        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id, targetroad, self.road, self.model.modelStepCount))
            exit()