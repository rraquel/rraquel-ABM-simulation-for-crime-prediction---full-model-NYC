#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psycopg2, sys, os, time, random, logging
from time import sleep

conn= psycopg2.connect("dbname='shared' user='rraquel' host='127.0.0.1' password='Mobil4b' ")
mycurs=conn.cursor()

print("start query")
#mycurs.execute("""Insert into abm_res.res_la_roadsprototype2 ("run_id","step","agent","road_id", i, trip)
#select run_id, step, agent, road_id, i, trip from abm_res.res_la_roadsprototype
#where run_id in (select run_id from abm_res.res_la_runprototype)""")

mycurs.execute("""DELETE FROM abm_res.res_la_roadsprototype
	WHERE run_id NOT IN (SELECT run_id FROM abm_res.res_la_runprototype)""")

conn.commit()
mycurs.execute("""DELETE FROM abm_res.res_la_agentprototype
	WHERE run_id NOT IN (SELECT run_id FROM abm_res.res_la_runprototype)""")
conn.commit()  
#mycurs.execute("""select * from abm_res.res_la_roadsprototype2 limit 10""")
result=mycurs.fetchall()
print(result[0])
conn.close()

