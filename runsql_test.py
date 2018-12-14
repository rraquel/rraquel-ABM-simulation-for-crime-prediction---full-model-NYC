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

run_id=620
table='abm_res.crimesperCTjune2015'
mycurs.execute("""Insert into {0} ("run_id"
            ) values
            ({1})""".format(table,             
            run_id))

#conn.commit()  
#mycurs.execute("""select * from abm_res.res_la_roadsprototype2 limit 10""")
print(result[0])
conn.close()

