import numpy as np
import math
import sys, psycopg2, os, time, random, logging
from operator import itemgetter
from collections import Counter

roads=[(7,0.001,None),(8,8,8)]
road=100    
    
    
def weightedChoice(roads, road):
    #TODO bring weihts to same scale!!!
    if not roads:
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
            weightList2=[float(i*100) for i in weightList2]
            weightList=[i*j for i,j in zip(weightList,weightList2)]
            #self.log.debug('combined weights: {}'.format(weightList[0]))
        pWeightList=[]
        sumWeightList=sum(weightList)
        for value in weightList:
            pWeightList.append(value/sumWeightList)
        #self.log.debug('weightlist p sum: {}'.format(sum(pWeightList)))
        roadIdNp=np.random.choice(roadsList, 1, True, pWeightList)
        roadId=roadIdNp[0]  
    return roadId

weightedChoice(roads, road)
print(weightedChoice(roads, road))