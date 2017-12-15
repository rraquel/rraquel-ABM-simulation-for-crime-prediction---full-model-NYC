#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections
import uuid




conn= psycopg2.connect("dbname='shared' user='rraquel' host='127.0.0.1' password='Mobil4b' ")        
mycurs = conn.cursor()

numagents=[5, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500]
numagents=[5, 25]

table="open.test"
mycurs.execute("""DROP TABLE {0}""".format(table))

mycurs.execute("""CREATE TABLE {0} (
        run_id integer)""".format(table))
conn.commit()
mycurs.execute("""Insert into {0} ("run_id") values({1})""".format(table,2))
conn.commit()
conn.close()


print('done')