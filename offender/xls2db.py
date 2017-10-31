#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, time, configparser
import logging
from Model import Model
import psycopg2, sys, os, time
from pandas import ExcelWriter
import pandas
from stat import ST_MTIME
from mesa.batchrunner import BatchRunner
from datetime import datetime

class Runner:
    def __init__(self,xlsfile):
        self.df_dict = pandas.read_excel(xlsfile,sheetname=None)
        self.model_df = self.df_dict['Model']
        self.agent_df = self.df_dict['Agent']
        
        self.timestamp = os.stat(xlsfile)[ST_MTIME]
        self.numAgents = self.df_dict['Model'].to_dict()['agentCount'][0]

        #print(self.df_dict['Model'].to_dict())
        self.connectDB()

    def connectDB(self):
        try:
            self.conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
            self.mycurs=self.conn.cursor()
            #self.log.info("connected to DB")
        except Exception as e:
            print("connection to DB failed"+str(e))
            sys.exit(1)
    
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
        print("Agents",agents)
        # Fields to be inserted
        insertf = self.getInsertFields(agents, 'res_la_agent')
        insertFieldStr = '"' + str.join('", "', insertf) + '"'
        for agentId in range(self.numAgents):
            for stepId in range(len(agents[insertf[0]])-1):
                print("stepId",stepId, agentId)
                insertValues = []
                for f in insertf:
                    insertValues.append( str(agents[f][(stepId, agentId)]) )
                insertValues = [str(self.run_id), str(stepId), str(agentId)] + insertValues
                insertValuesStr = str.join(", ", insertValues)
                sql = """insert into open.res_la_agent ("run_id","step","agent",{0}) values ({1})""".format(insertFieldStr, insertValuesStr )
                print("SQL: ", sql)
                self.mycurs.execute(sql)
        #self.model.conn.commit()
        print("End Agent data dumping")

    def getInsertFields(self,df_dict,tableName):
        """Compare DB Fields and data frame fields. If one of them is changed the program still works."""
        dbf = self.getTableFields(tableName)
        insertf=[]
        for f in dbf:
            if f in df_dict.keys() and not f in self.dbIgnoreFields:
                insertf.append( f )
            else:
                print("Field ignored: ", f)
        return(insertf)

    def writeDBmodel(self):
        """a"""
        print("Model Data Dumping")
        modelData = self.model_df.to_dict()
        # Fields to be inserted
        insertf = self.getInsertFieldsStr(modelData,'res_la_model')
        print("insertf",insertf)
        insertFieldStr = '"' + str.join('", "', insertf) + '"'
        for stepId in range(len(modelData[insertf[0]])):
            insertValues = []
            for f in insertf:
                insertValues.append( str(modelData[f][stepId]) )
            insertValues = [str(self.run_id), str(stepId)] + insertValues
            insertValuesStr = str.join(", ", insertValues)
            sql = """insert into open.res_la_model ("run_id","step","agent",{0}) values ({1})""".format(insertFieldStr, insertValuesStr )
            # print("SQL: ", sql)
            self.mycurs.execute(sql)
        self.conn.commit()

    def writeDBstart(self):
        self.dbIgnoreFields = ["run_id", "step", "agent"]
        sql = """insert into open.res_la_run values (DEFAULT, current_timestamp, NULL, {0}) 
            returning run_id""".format(self.numAgents)
        self.mycurs.execute(sql)
        self.run_id = self.mycurs.fetchone()[0]

    def writeDB(self):
        """Push data to DB"""
        self.writeDBagent()
        self.writeDBmodel()
        sql = """update open.res_la_run set end_date = current_timestamp where run_id={0}""".format(self.run_id)
        self.conn.commit()

if __name__ == '__main__':
    # Initialize variables so they can be used as global
    runner = Runner(sys.argv[1])
    runner.writeDBstart()
    runner.writeDB()
