#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, time, configparser
import logging
from Model import Model
import psycopg2, sys, os
from pandas import ExcelWriter
from mesa.batchrunner import BatchRunner

# Read the supplied config file or default config if none is supplied
def readConfig():
    """Find config file and read it"""
    #global variable
    global config
    #directory of current file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if len(sys.argv) > 1:
        #config folder and file
        cfile = os.path.join(dir_path,'..','config',sys.argv[1])
    else:
        cfile = os.path.join(dir_path,'..','config','default.ini')
    config = configparser.ConfigParser()
    config.read(cfile)

def writeExcel(model_df):
    """Create xls for later analysis"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    excelfile = os.path.join(dir_path,'..','output','offender.{}.xls'.format(time.strftime('%Y%m%d_%H%M%S')))
    excelwriter = ExcelWriter(excelfile)
    model_df.to_excel(excelwriter,sheet_name='Model')
    excelwriter.close()

log=logging.getLogger('')

#Batchrunner - Parameters
"""variable"""
# How many agents to create
#numAgents=1
# How many times does an agent travel
# afterwards a new start location is searched, effectively resetting the agent - 0 if no travel average desired
#agentTravelTrips=3.6
#type of starting location --- 0: RANDOM, 1: PLUTO
#startLocationType=1
#target type --- 0: Random ROAD, 1: Random VENUE, 2: Popular Venue- else defalut Agent
#targetType=2
#radius type --- 0: STATIC, 1: UNIFORM, 2: POWER
#radiusType=1


parameters1={"numAgents": 1,
"radiusType": 0,
"targetType": 0,
"startLocationType": 0,
"agentReturn": 0}

parameters2={"numAgents": range(1, 5),
"radiusType": range(0, 2),
"targetType": range(0, 2),
"startLocationType": range(0, 2),
"agentReturn": range(0, 1)}

batch_run=BatchRunner(Model, parameters1, iterations=1, max_steps=5, model_reporters={})
#model_reporters={"numAgents": lambda m: model.schedule.get_agent_count()}
batch_run.run_all()

# Initialize variables so they can be used as global

#statistics collection and data output
#get data as pandas data frame

print('model vars {}'.format(batch_run.iterations))


model_df=batch_run.get_model_vars_dataframe()
writeExcel(model_df)
log.info('Global stats: \n{}'.format(model_df.tail()))

print("end")