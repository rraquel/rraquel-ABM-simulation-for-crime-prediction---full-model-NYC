#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections
import uuid


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


def buildbase():
    #TODO erase run_id=622 - - - only for testing
    mycurs.execute("""SELECT run_id, num_agents, "distancetype", "targettype", "wayfindingtype", numsteps
        from abm_res.res_la_runprototype
        WHERE {0}""".format(select_ids))
    a=mycurs.fetchall() #returns tuple with first row (unordered list)
    #resultsList=[]
    result_id=0
    for line in a:
        #resultKey=line[0]
        #rArray=[line[1], line[2], line[3], int(line[4])]
        #configdict[resultKey]=rArray
        #for a in numagents:
        #results=Results(result_id, line[0], line[1], str(line[2]), str(line[3]), str(line[4]), int(line[5]), a)
        results=Results(result_id, line[0], line[1], str(line[2]), str(line[3]), str(line[4]), int(line[5]))
        resultsList.append(results)
        result_id+=1
        #print(results)
        #print(results.id)
        #print(results.result_id)
        #print(results._ID)
        #print(results.num_agents)
    print('done buildbase')


def allCrimesBaseline():
    run_id=0
    ctftus=dict()
    """select uniqueCrimes and cummCrimes"""
    mycurs.execute("""select count(distinct object_id), offense, new_gid, new_gid_ftus
        from open.nyc_road2censustract as c
	    left join open.nyc_road2pi_5ft_2015_jun j on j.road_id=c.gid
        where not offense is null group by new_gid, offense, new_gid_ftus""")
    res=mycurs.fetchall()

    print(run_id)
    d=dict()
    #tuple=(ctftus, crimecount, burglarycount, robberycount, larcenycount, larcenyMotorcount, assaultcount)
    for line in res:
        ct=line[2]
        if not ct in d:
            ctftus[ct]=line[3]
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
            mycurs.execute("""Insert into {0} ("run_id", ct , ct_ftus, totalcount,
            burglarycount, robberycount, larcenycount, larcenyMotorcount, assaultcount
            ) values
            ({1},{2},'{3}',{4},{5},{6},{7},{8},{9})""".format(
            table,             
            run_id, ct, ctftus[ct], d[ct]['totalcount'], d[ct]['burglarycount'], 
            d[ct]['robberycount'], d[ct]['larcenycount'], d[ct]['larcenyMotorcount'], d[ct]['assaultcount']))
        conn.commit()
    except:
        print("could not insert values in table ")
    conn.commit()

def allCrimes():
    #for x in numagents:
    #for each run_id
    for element in resultsList:
        run_id=element.run_id
        ctftus=dict()
        """select uniqueCrimes and cummCrimes"""
        mycurs.execute("""SELECT count(distinct object_id), offense, new_gid, new_gid_ftus FROM (
            SELECT distinct road_id FROM abm_res.res_la_roadsprototype where run_id={0}) AS rp
            left join open.nyc_road2pi_5ft_2015_jun AS j ON rp.road_id=j.road_id 
            left join open.nyc_road2censustract c ON j.road_id=c.gid where new_gid=17 group BY new_gid, offense, new_gid_ftus""".format(run_id))
        res=mycurs.fetchall()

        print(run_id)
        element.d=dict()
        #tuple=(ctftus, crimecount, burglarycount, robberycount, larcenycount, larcenyMotorcount, assaultcount)
        for line in res:
            ct=line[2]
            if not ct in element.d:
                ctftus[ct]=line[3]
                c=dict()
                c['totalcount']=0
                c['burglarycount']=0
                c['robberycount']=0
                c['larcenycount']=0
                c['larcenyMotorcount']=0
                c['assaultcount']=0
                element.d[ct]=c
            crimetype=line[1]
            if crimetype=='BURGLARY':
                burglarycount=line[0]
                element.d[ct]['burglarycount']+=burglarycount
                element.d[ct]['totalcount']+=burglarycount
            elif crimetype=='ROBBERY':
                robberycount=line[0]
                element.d[ct]['robberycount']+=robberycount
                element.d[ct]['totalcount']+=robberycount
            elif crimetype=='GRAND LARCENY':
                larcenycount=line[0]
                element.d[ct]['larcenycount']+=larcenycount
                element.d[ct]['totalcount']+=larcenycount
            elif crimetype=='GRAND LARCENY OF MOTOR VEHICLE':
                larcenyMotorcount=line[0]
                element.d[ct]['larcenyMotorcount']+=larcenyMotorcount
                element.d[ct]['totalcount']+=larcenyMotorcount
            elif crimetype=='FELONY ASSAULT': 
                assaultcount=line[0]
                element.d[ct]['assaultcount']+=assaultcount
                element.d[ct]['totalcount']+=assaultcount
        print(element.d[17], element.d[17]['totalcount'])            
        try:        
            for ct in element.d.keys():
                mycurs.execute("""Insert into {0} ("run_id", ct , ct_ftus, totalcount,
                burglarycount, robberycount, larcenycount, larcenyMotorcount, assaultcount
                ) values
                ({1},{2},'{3}',{4},{5},{6},{7},{8},{9})""".format(
                table,             
                run_id, ct, ctftus[ct], element.d[ct]['totalcount'], element.d[ct]['burglarycount'], 
                element.d[ct]['robberycount'], element.d[ct]['larcenycount'], element.d[ct]['larcenyMotorcount'], element.d[ct]['assaultcount']))
            conn.commit()
        except:
            print("could not insert values in table ")
        conn.commit()

def createNewTable():
    try:
        mycurs.execute("""DROP TABLE {0}""".format(table))
    except:
        print("table does not exist yet")
    mycurs.execute("""CREATE TABLE {0} (
        run_id integer,
        ct numeric,
        ct_ftus geometry,
        totalcount numeric,
        burglarycount numeric,
        robberycount numeric,
        larcenycount numeric,
        larcenyMotorcount numeric,
        assaultcount numeric)""".format(table))
    conn.commit()
    print("table created")


conn= psycopg2.connect("dbname='shared' user='rraquel' host='127.0.0.1' password='Mobil4b' ")        
mycurs = conn.cursor()

#numagents=[5, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000]
#for test
numagents=[5]
baseline='abm_res.crimesperCTjune2015'

roadsT='abm_res.res_la_roadsprototype2'
#table to save results
table='abm_res.crimesperCTjune2015'
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

createNewTable()
allCrimesBaseline()
    
#for test
#select_ids='run_id=620 OR run_id=62'
for id in list_ids:
    #select_ids="'run_id="+str(id)+"'"
    select_ids='run_id='+str(id)
    print(select_ids)
    resultsList=[]
    buildbase()
    allCrimes()

conn.close()

