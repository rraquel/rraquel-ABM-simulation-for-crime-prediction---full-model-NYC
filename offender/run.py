#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, time, configparser
import logging
from Model import Model
import psycopg2, sys, os, time
from pandas import ExcelWriter
from mesa.batchrunner import BatchRunner
from datetime import datetime

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

def writeExcel(agent_df,model_df):
    """Create xls for later analysis"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    excelfile = os.path.join(dir_path,'..','output','offender.{}.xls'.format(time.strftime('%Y%m%d_%H%M%S')))
    excelwriter = ExcelWriter(excelfile)
    model_df.to_excel(excelwriter,sheet_name='Model')
    agent_df.to_excel(excelwriter,sheet_name='Agent')
    excelwriter.close()


# Create model with it's street network, venues, agents, ...
def createModel():
    global model, config
    try: 
        modelCfg=config['model']
    except:
        log.error("Problem with config. section model")
        sys.exit(1)
    model=Model(modelCfg)

# Step through the model
def stepModel():
    global model, config
    #iterates for model steps
    i=0
    for i in range(config.getint('general','numSteps', fallback=1)):
        model.step(i, config.getint('general','numSteps'))
        log.debug("=> step {0} performed".format(i))
    #statistics collection and data output
    #get data as pandas data frame
    agent_df = model.dc.get_agent_vars_dataframe()
    model_df = model.dc.get_model_vars_dataframe()
    writeExcel(agent_df,model_df)
    log.debug(agent_df)
    log.info('Global stats: \n{}'.format(model_df.tail()))

#Batchrunner
#fixed_params={"numSteps": 5, "roadBoundingBoxRadius": 80, "staticRadius": 40000, "mu": 0.6, "dmin": 2.5, "dmax": 530}
#variable_params={"numAgents": range (4, 5), "startLocationType": range(0, 1), "targetType": range(0, 1), "radiusType": range(0,2)}

#batch_run=BatchRunner(Model, fixed_params, variable_params, max_steps=10
#)
# model_reporters=("numAngents": lambda m: model.schedule.get_agent_count)
#batch_run.run_all()


# Initialize variables so they can be used as global
model=""
config=""

log=logging.getLogger('')
#logging.basicConfig(stream=sys.stdout, level=logging.CRITICAL)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

t=time.monotonic()
print("time at start of model {}".format(str(time.monotonic()-t)))

readConfig()
print("Config read")

createModel()
print("time at model created {}".format(str(time.monotonic()-t)))

stepModel()
print("time at end of model {}".format(str(time.monotonic()-t)))
