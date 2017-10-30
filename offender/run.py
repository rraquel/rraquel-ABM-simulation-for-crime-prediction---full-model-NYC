#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, time, configparser
import logging
from Model import Model
import psycopg2, sys, os, time
from pandas import ExcelWriter
from mesa.batchrunner import BatchRunner
from datetime import datetime

class Runner:
    def __init__(self):
        # Initialize variables so they can be used as global
        self.model=""
        self.config=""
        self.log=logging.getLogger('')
        logging.basicConfig(stream=sys.stdout, level=logging.CRITICAL)
        #logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        self.t=time.monotonic()
        print("time at start of model {}".format(str(time.monotonic()-self.t)))

    def readConfig(self):
        """Find config file and read it"""
        #directory of current file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if len(sys.argv) > 1:
            #config folder and file
            cfile = os.path.join(dir_path,'..','config',sys.argv[1])
        else:
            cfile = os.path.join(dir_path,'..','config','default.ini')
        self.config = configparser.ConfigParser()
        self.config.read(cfile)

    def writeExcel(self):
        """Create xls for later analysis"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        excelfile = os.path.join(dir_path,'..','output','offender.{}.xls'.format(time.strftime('%Y%m%d_%H%M%S')))
        excelwriter = ExcelWriter(excelfile)
        self.model_df.to_excel(excelwriter,sheet_name='Model')
        self.agent_df.to_excel(excelwriter,sheet_name='Agent')
        excelwriter.close()

    def writeDB(self):
        """Drop data to DB"""
        sql = """insert into open.res_la_run values (NULL, current_timestamp, NULL, 0) returning run_id"""
        mycurs = self.model.conn.cursor()
        mycurs.execute(sql)
        run_id = mycurs.fetchone()[0]

    # Create model with it's street network, venues, agents, ...
    def createModel(self):
        try: 
            modelCfg=self.config['model']
        except Exception as e:
            self.log.error("Problem with config. section model {}".format(e))
            sys.exit(1)
        self.model=Model(modelCfg)

    # Step through the model
    def stepModel(self):
        #iterates for model steps
        i=0
        for i in range(self.config.getint('general','numSteps', fallback=1)):
            self.model.step(i, self.config.getint('general','numSteps'))
            self.log.debug("=> step {0} performed".format(i))
        #statistics collection and data output
        #get data as pandas data frame
        self.agent_df = self.model.dc.get_agent_vars_dataframe()
        self.model_df = self.model.dc.get_model_vars_dataframe()
        self.writeExcel()
        self.writeDB()
        self.log.debug(self.agent_df)
        self.log.info('Global stats: \n{}'.format(self.model_df.tail()))

#Batchrunner
#fixed_params={"numSteps": 5, "roadBoundingBoxRadius": 80, "staticRadius": 40000, "mu": 0.6, "dmin": 2.5, "dmax": 530}
#variable_params={"numAgents": range (4, 5), "startLocationType": range(0, 1), "targetType": range(0, 1), "radiusType": range(0,2)}

#batch_run=BatchRunner(Model, fixed_params, variable_params, max_steps=10
#)
# model_reporters=("numAngents": lambda m: model.schedule.get_agent_count)
#batch_run.run_all()


if __name__ == '__main__':
    # Initialize variables so they can be used as global
    runner = Runner()

    runner.readConfig()
    print("Config read")

    runner.createModel()
    print("time at model created {}".format(str(time.monotonic()-runner.t)))

    runner.stepModel()
    print("time at end of model {}".format(str(time.monotonic()-runner.t)))
