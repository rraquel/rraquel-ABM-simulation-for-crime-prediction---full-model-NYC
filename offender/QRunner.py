#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This code is intended to make db calls more parallel
# One shot db queries can be executed (probably insert)

import multiprocessing
import time
import psycopg2
import os
import time
import configparser
from psycopg2.pool import ThreadedConnectionPool

class Consumer(multiprocessing.Process):
    def __init__(self, task_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue

    def run(self):
        proc_name = self.name
        print('Consumer Initialized')
        while True:
            next_task = self.task_queue.get()
            print("Got Task from queue")
            if next_task is None:
                print("Got None, closing queue")
                self.task_queue.task_done()
                break            
            Task(next_task)
            self.task_queue.task_done()

class Task(object):
    pool = ""
    def __init__(self, runRoads):
        self.runRoads = runRoads
        self.pool = Task.pool

    def __call__(self):        
        pyConn = Task.pool.getconn()
        pyConn.set_session(autocommit=False)
        pyCursor1 = pyConn.cursor()
        for road in self.runRoads['way']:
            procQuery = """insert into open.tmp_res_roads ("id","run_id","step","agent","road_id") values
                    (DEFAULT,{0},{1},{2},{3} )""".format(self.runRoads['run_id'], self.runRoads['step'], self.runRoads['agent'], road)
            pyCursor1.execute(procQuery)
        pyConn.commit()
        Task.pool.putconn(pyConn)
        return(0)

    def __str__(self):
        return('ARC')

    def run(self):
        pass

class QRunner:
    def __init__(self):
        print('Initializing QRunner')
        self.tasks = multiprocessing.JoinableQueue()
        self.num_consumers = 2 #multiprocessing.cpu_count()
        config = configparser.ConfigParser()
        config.read('config/dbconn.ini')
        dbCfg = config['general']
        dsn = "dbname='" + dbCfg.get('dbname', 'shared') + "' user='" + dbCfg.get('user') + "' host='" + dbCfg.get('host',
            'localhost') + "' port='" + str(dbCfg.getint('port', 5432)) + "' password='" + dbCfg.get('password') + "'"
        Task.pool = ThreadedConnectionPool(self.num_consumers, self.num_consumers *2, dsn)
        # Start the queue consumers to watch the tasks-queue
        consumers = [Consumer(self.tasks) for i in range(self.num_consumers)]
        for w in consumers:
            w.start()
    
    def store_roads(self, runRoads):
        """Put array of one step's roads into the database
        Input: {"run_id": 3, "step": 7, "agent":9, "way":[1,4,7,9] }  """
        print("Putting Task on Queue")
        self.tasks.put(runRoads)

    def exit(self):
        """Cleanup the queue, so it does not block on exit and so you know all queues are empty"""
        print('Cleaning up QRunner')
        for i in range(self.num_consumers):
            self.tasks.put(None)

# if __name__ == '__main__':    
#     pyConnX = psycopg2.connect("dbname='geobase_1' host = 'localhost'")
#     pyConnX.set_isolation_level(0)
#     pyCursorX = pyConnX.cursor()

#     pyCursorX.execute('SELECT count(*) FROM cities WHERE gid_fkey IS NULL')    
#     temp = pyCursorX.fetchall()    
#     num_job = temp[0]
#     num_jobs = num_job[0]

#     pyCursorX.execute('SELECT city_id FROM city WHERE gid_fkey IS NULL')    
#     cityIdListTuple = pyCursorX.fetchall()    

#     cityIdList = []

#     for x in cityIdListTuple:
#         cityIdList.append(x[0])

#     for i in xrange(num_jobs):
#         tasks.put(Task(cityIdList[i - 1]))

#     for i in xrange(num_consumers):
#         tasks.put(None)

#     while num_jobs:
#         result = results.get()
#         num_jobs -= 1
