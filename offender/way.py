#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mesa
from mesa.time import RandomActivation
import Model
import networkx as nx
import numpy as np
import math
from collections import OrderedDict
import sys, psycopg2, os, time, random, logging
from operator import itemgetter
import globalVar


class Way:
    """agent path options"""
    def __init__(self, unique_id, model, road):
        self.log=logging.getLogger('')
        self.unique_id=unique_id
        self.model=model
        self.wayfindingType=model.wayfindingType
        self.road=road
        self.way=[]

    def waybytype(self, targetroad):
        getattr(self, self.wayfindingType)(targetroad)
        return self.way

    def wayLength(self, targetroad):
        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            #roads are represented as nodes in G
            self.way=nx.shortest_path(self.model.G,self.road,targetroad,weight='length')
            #print("Agent ({0}) way: {1}".format(self.unique_id,self.way))

        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id, targetroad, self.road, self.model.modelStepCount))
            exit()

    def wayWidth(self, targetroad):
        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            #roads are represented as nodes in G
            self.way=nx.shortest_path(self.model.G,self.road,targetroad,weight='width')
            #print("Agent ({0}) way: {1}".format(self.unique_id,self.way))

        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id, targetroad, self.road, self.model.modelStepCount))
            exit()

    def wayLengthWidth(self, targetroad):
        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            #roads are represented as nodes in G
            self.way=nx.shortest_path(self.model.G,self.road,targetroad,weight='length')
            #print("Agent ({0}) way: {1}".format(self.unique_id,self.way))

        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id, targetroad, self.road, self.model.modelStepCount))
            exit()

    def wayRoadtype(self, targetroad):
        """find way using road lenght"""
        #self.log.debug('search radius: {}'.format(self.radiusR))
        try:
            #roads are represented as nodes in G
            self.way=nx.shortest_path(self.model.G,self.road,targetroad,weight='length')
            #print("Agent ({0}) way: {1}".format(self.unique_id,self.way))

        except Exception as e:
            self.log.critical("trip: Error: wayfinding: agent id {0}, current road: {2} targetRoad {1}, stepcount: {3}".format(self.unique_id, targetroad, self.road, self.model.modelStepCount))
            exit()
