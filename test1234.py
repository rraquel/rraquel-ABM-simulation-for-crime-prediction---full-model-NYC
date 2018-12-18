import networkx as nx
import psycopg2, sys, os, time, random, logging

conn= psycopg2.connect("dbname='shared' user='rraquel' host='127.0.0.1' password='Mobil4b' ")
mycurs=conn.cursor()

table2='abm_res.crimesperCTdiff'
run_id=0
ct=2
a='diff'
dnew=99


mycurs.execute("""Insert into {0} ("run_id", ct, numagents, atype, totaldiff,
                burglarydiff, robberydiff, larcenydiff, larcenyMotordiff, assaultdiff
                ) values
                ({1},{2}, {3}, '{4}', {5}, {6}, {7}, {8}, {9}, {10})""".format(
                table2,             
                run_id, ct, 1000, a, dnew, dnew, 
                dnew, dnew, dnew, dnew))
conn.commit()
conn.close()
