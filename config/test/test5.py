
import random
import sys, psycopg2, os, time, random, logging
import networkx as nx
from random import choices
import pandas as pd
import numpy as np
import pylab as pl
from collections import Counter
from datetime import datetime

import psycopg2; print(psycopg2.__version__)


def connectDB():
        try:
            conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
            curs=conn.cursor()
            logging.info("connected to DB")
        except Exception as e:
            logging.debug("not connected")
        return conn


conn=connectDB()
curs = conn.cursor()

run=1
step=5
way=[100, 200, 300, 400, 500]

curs.execute_batch("""insert into open.test ("run","step","road") values 
            ({0},{1},{2})""".format(run, step, way))
#curs.execute( """insert into open.test ("run","step","road") values 
#            ({0},{1},{2})""".format(run, step, way))
            #Remove if not DB writing-
