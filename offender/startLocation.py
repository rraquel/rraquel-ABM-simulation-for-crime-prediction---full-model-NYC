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


"""find start location of agent"""
log=logging.getLogger('')

#crimes=[]
#for i in range(6):
#    crimes.append([])
    
##select starting position by type

startRoad=0

#allCrimes=model.allCrimes
#statistics
#self.crimes=Counter()
        


def findStartLocation(model, startType, unique_id):
    #print("startLocationType {}".format(policeStartType))
    string=str(eval(startType)(model, unique_id))
    startRoad=eval(string)
    #print(startRoad)
    log.debug("startRoad: {0}".format(startRoad))
    #targetRoadList.append(startRoad)
    return startRoad
    
def findStartRandom(model, unique_id):
    """select startingPoint from random sample of nodes"""
    #print("in start random")
    return np.random.choice(model.G.nodes(),1)[0]

def findStartResidence(model, unique_id):
    """Select startRoad within Residential Areas from PlutoMap"""
    roadIdNp=np.random.choice(model.residentRoads,1)
    startRoad=roadIdNp[0]
    return startRoad


def findStartResidencePopulation(model, unique_id):
    """Select startRoad within Residential Areas from PlutoMap and population density"""
    roadIdNp=np.random.choice(model.residentRoads, 1, True, model.residentRoadsWeight)
    startRoad=roadIdNp[0]
    return startRoad
