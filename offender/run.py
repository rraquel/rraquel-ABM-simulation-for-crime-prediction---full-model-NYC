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
            self.cfile = os.path.join(dir_path,'..','config',sys.argv[1])
        else:
            self.cfile = os.path.join(dir_path,'..','config','default.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.cfile)
        # Add dbconfig
        cfg = configparser.ConfigParser()
        cfg.read(os.path.join(dir_path, '..', 'config', 'dbconn2.ini'))
        dbCfg = cfg['general']
        self.config.set('model', 'dsn', "dbname='" + dbCfg.get('dbname', 'shared') + "' user='" + dbCfg.get('user') + "' host='" + dbCfg.get('host',
            'localhost') + "' port='" + str(dbCfg.getint('port', 5432)) + "' password='" + dbCfg.get('password') + "'")

    def writeExcel(self):
        """Create xls for later analysis"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        excelfile = os.path.join(dir_path,'..','output','offender.{}.xls'.format(time.strftime('%Y%m%d_%H%M%S')))
        excelwriter = ExcelWriter(excelfile)
        self.model_df.to_excel(excelwriter,sheet_name='Model')
        self.agent_df.to_excel(excelwriter,sheet_name='Agent')
        excelwriter.close()

    def getTableFields(self,tableName):
        sql = """select column_name from information_schema.columns where data_type='numeric' and
        table_name='{0}'""".format(tableName)
        self.mycurs.execute(sql)
        columns = self.mycurs.fetchall()
        return([x[0] for x in columns])

    def writeDBagent(self):
        """a"""
        print("Agent Data Dumping")
        agents = self.agent_df.to_dict()
        # Fields to be inserted
        insertf = self.getInsertFields(agents, 'res_la_agentprototype')
        insertFieldStr = '"' + str.join('", "', insertf) + '"'
        for agentId in range(self.model.numAgents):
            for stepId in range(int(round(len(agents[insertf[0]]) / self.model.numAgents))):
                insertValues = []
                for f in insertf:
                    insertValues.append( str(agents[f][(stepId, agentId)]) )
                insertValues = [str(self.run_id), str(stepId), str(agentId)] + insertValues
                insertValuesStr = str.join(", ", insertValues)
                sql = """insert into abm_res.res_la_agentprototype ("run_id","step","agent",{0}) values ({1})""".format(insertFieldStr, insertValuesStr )
                self.mycurs.execute(sql)
        #self.model.conn.commit()
        print("End Agent data dumping")

    def getInsertFields(self,df_dict,tableName):
        """Compare DB Fields and data frame fields. If one of them is changed the program still works."""
        dbf = self.getTableFields(tableName)
        insertf=[]
        for f in dbf:
            try:
                f = str(f)
                if f in df_dict.keys() and not f in self.dbIgnoreFields:
                    insertf.append( f )
                else:
                    self.log.warn("Field ignored: {}".format(f))
            except:
                pass
        return(insertf)

    def writeDBmodel(self):
        """a"""
        print("Model Data Dumping")
        modelData = self.model_df.to_dict()
        # Fields to be inserted
        insertf = self.getInsertFields(modelData,'res_la_modelprototype')
        #print("insertf",insertf)
        insertFieldStr = '"' + str.join('", "', insertf) + '"'
        for stepId in range(len(modelData[insertf[0]])):
            insertValues = []
            for f in insertf:
                insertValues.append( str(modelData[f][stepId]) )
            insertValues = [str(self.run_id), str(stepId)] + insertValues
            insertValuesStr = str.join(", ", insertValues)
            sql = """insert into abm_res.res_la_modelprototype("run_id","step",{0}) values ({1})""".format(insertFieldStr, insertValuesStr )
            #print("SQL: ", sql)
            self.mycurs.execute(sql)
        self.model.conn.commit()

    def writeDBstart(self):
        self.mycurs = self.model.conn.cursor()
        self.dbIgnoreFields = ["run_id", "step", "agent"]
        sql = """insert into abm_res.res_la_runprototype values (DEFAULT, current_timestamp, NULL, {0}, '{1}', '{2}','{3}','{4}','{5}', {6}, {7}, {8}, {9}) 
            returning run_id""".format(self.model.schedule.get_agent_count(),self.cfile,self.model.startLocationType,
              self.model.distanceType, self.model.targetType, self.model.wayfindingType, self.model.agentTravelAvg,
              self.model.staticRadius, self.model.mu, self.config.getint('general','numSteps', fallback=1))
        self.mycurs.execute(sql)
        self.run_id = self.mycurs.fetchone()[0]
        self.model.run_id = self.run_id
        print("run_id: {}".format(self.run_id))
        self.model.conn.commit()

    def writeDB(self):
        """Push data to DB"""
        self.writeDBagent()
        #not needed as model setup is written in run
        #self.writeDBmodel()
        sql = """update abm_res.res_la_runprototype set end_date = current_timestamp where run_id={0}""".format(self.run_id)
        self.mycurs.execute(sql)
        self.model.conn.commit()

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
            self.model.conn.commit()
        #statistics collection and data output
        #runner.model.insertQ.exit()
        #get data as pandas data frame
        self.agent_df = self.model.dc.get_agent_vars_dataframe()
        self.model_df = self.model.dc.get_model_vars_dataframe()
        try:
            self.writeExcel()
        except Exception as e:
            self.log.warn(e)
        try:
            self.writeDB()
        except Exception as e:
            print("Exception in writeDB",e)
        #self.log.debug(self.agent_df)
        self.log.info('Global stats: \n{}'.format(self.model_df.tail()))

if __name__ == '__main__':
    # Initialize variables so they can be used as global
    runner = Runner()
    print("prototype branch taxiData")
    runner.readConfig()
    print("Config read")

    runner.createModel()
    print("time at model created {}".format(str(time.monotonic()-runner.t)))

    runner.writeDBstart()

    # If you need profiling use the following lines
    # import cProfile
    # cProfile.run('runner.stepModel()','profiler_stats')
    #then run readstats.py

    runner.stepModel()
    print("time at end of model {}".format(str(time.monotonic()-runner.t)))
    