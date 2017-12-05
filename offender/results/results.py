import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections


conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
mycurs = conn.cursor()


class Results():
    """object containing each Scenario's results"""
    def __init__(self, run_id, num_agents, radiusType, targetType, num_steps):
        self.run_id=run_id
        self.num_agents=num_agents
        self.radiusType=radiusType
        self.targetType=targetType
        self.num_steps=num_steps

def calculatePAI():
    pass



mycurs.execute("""SELECT m.run_id, m.num_agents, r."radiustype", r."targettype", num_steps
    from open.res_la_run
    WHERE (run_id=320 OR   
    run_id=321 OR
    run_id=325 OR
    run_id=326 OR
    run_id=327 OR
    run_id=328 OR
    run_id=330 OR
    run_id=331 OR
    run_id=332 OR
    run_id=333 OR
    run_id=334 OR
    run_id=335 OR
    run_id=336 OR
    run_id=337 OR
    run_id=338)""")
results=mycurs.fetchall() #returns tuple with first row (unordered list)

for line in results:
    r=Results(line[0], line[1], line[2], line[3], line[4])
    print(r)
#calculatePAI()