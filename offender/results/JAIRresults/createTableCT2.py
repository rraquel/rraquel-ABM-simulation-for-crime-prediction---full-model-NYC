#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections
import uuid


"""Older version but works good!!! """

class Results():
    """object containing each Scenario's results"""
    _ID = 0
    def __init__(self, result_id, run_id, totalnumagents, distanceType, targetType, wayfindingType, numsteps):
        self.result_id=result_id
        self.id = self._ID; self.__class__._ID += 1

        self.run_id=run_id
        self.totalnumagents=totalnumagents
        self.distanceType=distanceType
        self.targetType=targetType
        self.wayfindingType=wayfindingType
        self.numsteps=numsteps


        self.d=dict()



def allCrimesBaseline():
    print("start baseline")
    """select uniqueCrimes and cummCrimes"""
    mycurs.execute("""select count(distinct object_id), offense, new_gid, new_gid_ftus
        from open.nyc_road2censustract as c
	    left join open.nyc_road2pi_5ft_2015_jun j on j.road_id=c.gid
        where not offense is null group by new_gid, offense, new_gid_ftus""")
    res=mycurs.fetchall()
    d=dict()
    #tuple=(ctftus, crimecount, burglarycount, robberycount, larcenycount, larcenyMotorcount, assaultcount)
    for line in res:
        ct=line[2]
        if not ct in d:
            c=dict()
            c['totalcount']=0
            c['burglarycount']=0
            c['robberycount']=0
            c['larcenycount']=0
            c['larcenyMotorcount']=0
            c['assaultcount']=0
            d[ct]=c
        crimetype=line[1]
        if crimetype=='BURGLARY':
            burglarycount=line[0]
            d[ct]['burglarycount']+=burglarycount
            d[ct]['totalcount']+=burglarycount
        elif crimetype=='ROBBERY':
            robberycount=line[0]
            d[ct]['robberycount']+=robberycount
            d[ct]['totalcount']+=robberycount
        elif crimetype=='GRAND LARCENY':
            larcenycount=line[0]
            d[ct]['larcenycount']+=larcenycount
            d[ct]['totalcount']+=larcenycount
        elif crimetype=='GRAND LARCENY OF MOTOR VEHICLE':
            larcenyMotorcount=line[0]
            d[ct]['larcenyMotorcount']+=larcenyMotorcount
            d[ct]['totalcount']+=larcenyMotorcount
        elif crimetype=='FELONY ASSAULT': 
            assaultcount=line[0]
            d[ct]['assaultcount']+=assaultcount
            d[ct]['totalcount']+=assaultcount  
    try:        
        for ct in d.keys():
            mycurs.execute("""Insert into {0} ("run_id", ct , numagents, totalcount,
            burglarycount, robberycount, larcenycount, larcenyMotorcount, assaultcount
            ) values
            ({1},{2},{3},{4},{5},{6},{7},{8},{9})""".format(
            table,             
            0, ct, 0, d[ct]['totalcount'], d[ct]['burglarycount'], 
            d[ct]['robberycount'], d[ct]['larcenycount'], d[ct]['larcenyMotorcount'], d[ct]['assaultcount']))
        conn.commit()
    except:
        print("could not insert values in table ")
    print('done build baseline for all crimes')

def allCrimes(run_id, numagents):
    print("start all crimes")
    #for x in numagents:
    #for each run_id
    d=dict()
    """select uniqueCrimes and cummCrimes"""
    mycurs.execute("""SELECT count(distinct object_id), offense, new_gid FROM (
        SELECT distinct road_id FROM {0} where run_id={1}  and agent<{2}) AS rp
        left join open.nyc_road2pi_5ft_2015_jun AS j ON rp.road_id=j.road_id 
        left join open.nyc_road2censustract c ON j.road_id=c.gid where new_gid is not Null group BY new_gid, offense, new_gid_ftus""".format(roadsT, str(run_id), numagents))
    res=mycurs.fetchall()
    #tuple=(ctftus, crimecount, burglarycount, robberycount, larcenycount, larcenyMotorcount, assaultcount)
    for line in res:
        ct=line[2]
        if not ct in d:
            c=dict()
            c['totalcount']=0
            c['burglarycount']=0
            c['robberycount']=0
            c['larcenycount']=0
            c['larcenyMotorcount']=0
            c['assaultcount']=0
            d[ct]=c
        crimetype=line[1]
        if crimetype=='BURGLARY':
            burglarycount=line[0]
            d[ct]['burglarycount']+=burglarycount
            d[ct]['totalcount']+=burglarycount
        elif crimetype=='ROBBERY':
            robberycount=line[0]
            d[ct]['robberycount']+=robberycount
            d[ct]['totalcount']+=robberycount
        elif crimetype=='GRAND LARCENY':
            larcenycount=line[0]
            d[ct]['larcenycount']+=larcenycount
            d[ct]['totalcount']+=larcenycount
        elif crimetype=='GRAND LARCENY OF MOTOR VEHICLE':
            larcenyMotorcount=line[0]
            d[ct]['larcenyMotorcount']+=larcenyMotorcount
            d[ct]['totalcount']+=larcenyMotorcount
        elif crimetype=='FELONY ASSAULT': 
            assaultcount=line[0]
            d[ct]['assaultcount']+=assaultcount
            d[ct]['totalcount']+=assaultcount       
    try:        
        for ct in d.keys():
            mycurs.execute("""Insert into {0} ("run_id", ct , numagents, totalcount,
            burglarycount, robberycount, larcenycount, larcenyMotorcount, assaultcount
            ) values
            ({1},{2},{3},{4},{5},{6},{7},{8},{9})""".format(
            table,             
            run_id, ct, numagents, d[ct]['totalcount'], d[ct]['burglarycount'], 
            d[ct]['robberycount'], d[ct]['larcenycount'], d[ct]['larcenyMotorcount'], d[ct]['assaultcount']))
            conn.commit()
    except:
        print("could not insert values in table ")
        exit()

def completeCT(run_id, numagents):
    print("complete table")
    """insert ct if they have no crimes, to have complete map"""
    mycurs.execute("""INSERT INTO {0}
        SELECT {1}, gid, {2}, 0, 0, 0, 0, 0, 0 FROM open_shapes.nyc_census_tract_e
        WHERE gid NOT IN (SELECT ct FROM {3} WHERE run_id={4})""".format(table, str(run_id), numagents, table, str(run_id)))
    conn.commit()


def crimesCalc(run_id, numagents):
    mycurs.execute("""SELECT run_id, ct, numagents,
    totalcount, burglarycount, robberycount, larcenycount,
    larcenyMotorcount, assaultcount FROM {0} where run_id=0""".format(table))
    res0=mycurs.fetchall()
    db=dict()
    for line in res0:
        c=dict()
        ct=line[1]
        c['totalcount']=line[3]
        c['burglarycount']=line[4]
        c['robberycount']=line[5]
        c['larcenycount']=line[6]
        c['larcenyMotorcount']=line[7]
        c['assaultcount']=line[8]
        db[ct]=c

    mycurs.execute("""SELECT run_id, ct, numagents,
    totalcount, burglarycount, robberycount, larcenycount,
    larcenyMotorcount, assaultcount FROM {0} where run_id={1} and numagents={2}""".format(table, run_id, numagents))
    res=mycurs.fetchall()
    d=dict()
    for line in res:
        run_id=line[0]
        c=dict()
        ct=line[1]
        c['totalcount']=line[3]
        c['burglarycount']=line[4]
        c['robberycount']=line[5]
        c['larcenycount']=line[6]
        c['larcenyMotorcount']=line[7]
        c['assaultcount']=line[8]
        d[ct]=c

    crimesPercent(d, db)
    print("inserted new values in table 2")
    
    crimesDiff(d, db)
    print("inserted new values in table 2")
    

def crimesPercent(d, db):
    diff=dict()
    dnew=dict()
    a='percent'
    for ct in db.keys():
        print(db[ct])
        if db[ct]['totalcount']==0:
             diff['totaldiff']=0
        else:
            diff['totaldiff']=d[ct]['totalcount']*100/db[ct]['totalcount']
        if db[ct]['burglarycount']==0:
                 diff['burglarydiff']=0
        else:
            diff['burglarydiff']=d[ct]['burglarycount']*100/db[ct]['burglarycount']
        if db[ct]['robberycount']==0:
                 diff['robberydiff']=0
        else:
            diff['robberydiff']=d[ct]['robberycount']*100/db[ct]['robberycount']
        if db[ct]['larcenycount']==0:
                 diff['larcenydiff']=0
        else:
            diff['larcenydiff']=d[ct]['larcenycount']*100/db[ct]['larcenycount']
        if db[ct]['larcenyMotorcount']==0:
                 diff['larcenyMotordiff']=0
        else:
            diff['larcenyMotordiff']=d[ct]['larcenyMotorcount']*100/db[ct]['larcenyMotorcount']
        if db[ct]['assaultcount']==0:
                 diff['assaultdiff']=0
        else:
            diff['assaultdiff']=d[ct]['assaultcount']*100/db[ct]['assaultcount']
        dnew[int(ct)]=diff

        mycurs.execute("""Insert into {0} ("run_id", ct, numagents, atype, totaldiff,
            burglarydiff, robberydiff, larcenydiff, larcenyMotordiff, assaultdiff
            ) values
            ({1},{2},{3}, '{4}', {5}, {6}, {7}, {8}, {9}, {10})""".format(
            table2,             
            run_id, ct, 1000, a, diff['totaldiff'], diff['burglarydiff'], 
            diff['robberydiff'], diff['larcenydiff'], diff['larcenyMotordiff'],diff['assaultdiff']))
        conn.commit()

def crimesDiff(d, db):
    diff=dict()
    dnew=dict()
    a='difference'
    for ct in db.keys():
        if db[ct]['totalcount']==0:
             diff['totaldiff']=0
        else:
            diff['totaldiff']=d[ct]['totalcount']-db[ct]['totalcount']
        if db[ct]['burglarycount']==0:
                 diff['burglarydiff']=0
        else:
            diff['burglarydiff']=d[ct]['burglarycount']-db[ct]['burglarycount']
        if db[ct]['robberycount']==0:
                 diff['robberydiff']=0
        else:
            diff['robberydiff']=d[ct]['robberycount']-db[ct]['robberycount']
        if db[ct]['larcenycount']==0:
                 diff['larcenydiff']=0
        else:
            diff['larcenydiff']=d[ct]['larcenycount']-db[ct]['larcenycount']
        if db[ct]['larcenyMotorcount']==0:
                 diff['larcenyMotordiff']=0
        else:
            diff['larcenyMotordiff']=d[ct]['larcenyMotorcount']-db[ct]['larcenyMotorcount']
        if db[ct]['assaultcount']==0:
                 diff['assaultdiff']=0
        else:
            diff['assaultdiff']=d[ct]['assaultcount']-db[ct]['assaultcount']
        dnew[int(ct)]=diff
        mycurs.execute("""Insert into {0} ("run_id", ct, numagents, atype, totaldiff,
            burglarydiff, robberydiff, larcenydiff, larcenyMotordiff, assaultdiff
            ) values
            ({1},{2},{3}, '{4}', {5}, {6}, {7}, {8}, {9}, {10})""".format(
            table2,             
            run_id, ct, 1000, a, dnew[ct]['totaldiff'], dnew[ct]['burglarydiff'], 
            dnew[ct]['robberydiff'], dnew[ct]['larcenydiff'], dnew[ct]['larcenyMotordiff'], dnew[ct]['assaultdiff']))
        conn.commit()
    

def addftus(table, table2):
    tables=[table, table2]
    try:
        mycurs.execute("""ALTER TABLE {0}
            ADD COLUMN ftus geometry""".format(t))
        conn.commit()
    except:
        pass
    for t in tables:
        mycurs.execute("""UPDATE {}
	        SET ftus=ct.geom
	        from ( SELECT gid, geom from open_shapes.nyc_census_tract_e) ct
            where ct.gid={}.ct""".format(t,t))
        conn.commit()


def createNewTable():
    try:
        mycurs.execute("""DROP TABLE {0}""".format(table))
    except:
        print("table does not exist yet")
    mycurs.execute("""CREATE TABLE {0} (
        run_id integer,
        ct numeric,
         numagents numeric,
        totalcount numeric,
        burglarycount numeric,
        robberycount numeric,
        larcenycount numeric,
        larcenyMotorcount numeric,
        assaultcount numeric)""".format(table))
    conn.commit()
    print("table created")

def createNewTable2():
    try:
        mycurs.execute("""DROP TABLE {0}""".format(table2))
    except:
        print("table does not exist yet")
    mycurs.execute("""CREATE TABLE {0} (
        run_id integer,
        ct numeric,
        numagents numeric,
        atype varchar,
        totaldiff numeric,
        burglarydiff numeric,
        robberydiff numeric,
        larcenydiff numeric,
        larcenyMotordiff numeric,
        assaultdiff numeric)""".format(table2))
    conn.commit()
    print("table created")


conn= psycopg2.connect("dbname='shared' user='rraquel' host='127.0.0.1' password='Mobil4b' ")        
mycurs = conn.cursor()

#numagents=[5, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000]
#for test
numagents=1000
baseline='abm_res.crimesperCTjune2015'

#table to save results
table='abm_res.crimesperCTjune2015'
table2='abm_res.crimesperCTdiff'
#select_ids='(run_id=726 OR run_id=727)'
#select_ids='(run_id>734 and run_id<743)
 
#mapped crimes for June 2015
crimesTotal=8494
burglaryTotal=1287
robberyTotal=1301
larcenyTotal=3555
larcenyMTotal=580
assaultTotal=1778

list_ids=list()
#run 697 and 698
#620-636
#639-643
#664-691
#726-746
for id in range(620,637):
    list_ids.append(id)
for id in range(639,644):
    list_ids.append(id)
for id in range(664,692):
    list_ids.append(id)
for id in range(726,747):
    list_ids.append(id)

#createNewTable()
#createNewTable2()
#allCrimesBaseline()
#completeCT(0, 0)

list_ids=[620, 625, 664, 633, 739]
list_ids=[739]
numagents=300
    
#for test
#select_ids='run_id=620 OR run_id=62'
for id in list_ids:
    #select_ids="'run_id="+str(id)+"'"
    if id>725:
        roadsT='abm_res.res_la_roadsprototype2'
    else:
        roadsT='abm_res.res_la_roadsprototype'
    run_id=id

    allCrimes(run_id, numagents)
    completeCT(run_id, numagents)
    crimesCalc(run_id, numagents)

addftus(table, table2)   

conn.close()

