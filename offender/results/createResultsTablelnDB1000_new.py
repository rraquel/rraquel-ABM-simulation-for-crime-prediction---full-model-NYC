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
    def __init__(self, result_id, run_id, totalnumagents, distanceType, targetType, wayfindingType, numsteps, num_agents):
        self.result_id=result_id
        self.id = self._ID; self.__class__._ID += 1

        self.run_id=run_id
        self.totalnumagents=totalnumagents
        self.distanceType=distanceType
        self.targetType=targetType
        self.wayfindingType=wayfindingType
        self.numsteps=numsteps
        self.num_agents=num_agents

        self.uniqueCrimes=0
        self.BurglaryUniq=0
        self.RobberyUniq=0
        self.LarcenyUniq=0
        self.LarcenyMotorUnique=0
        self.AssaultUnique=0

        self.PercentuniqueCrimes=0.0
        self.PercentBurglaryUniq=0.0
        self.PercentRobberyUniq=0.0
        self.PercentLarcenyUniq=0.0
        self.PercentLarcenyMotorUnique=0.0
        self.PercentAssaultUnique=0.0

        self.uniqPai=0
        self.uniquePaiBurglary=0
        self.uniquePaiRobbery=0
        self.uniquePaiLarceny=0
        self.uniquePaiLarcneyM=0
        self.uniquePaiAssault=0
        self.walkedD=0
        self.walkedDPercent=0

        self.cummCrimes=0
        self.BurglaryCumm=0
        self.RobberyCumm=0
        self.LarcenyCumm=0
        self.LarcenyMotorCumm=0
        self.AssaultCumm=0



def buildbase():
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
        for a in numagents:
            results=Results(result_id, line[0], line[1], str(line[2]), str(line[3]), str(line[4]), int(line[5]), a)
            resultsList.append(results)
            result_id+=1
            #print(results)
            #print(results.id)
            #print(results.result_id)
            #print(results._ID)
            #print(results.num_agents)
    print('done')

def distance():
    for x in numagents:
        """select uniqueCrimes and cummCrimes"""
        mycurs.execute("""SELECT run_id, sum(distinct(shape_leng)) AS distinctSum FROM
        (SELECT run.run_id, run.road_id, road.shape_leng from abm_res.res_la_roadsprototype run
        LEFT JOIN open.nyc_road_proj_final as road on road.gid=run.road_id WHERE run.agent<{0} and {1})
        as f group by f.run_id""".format(x,select_ids))
        a=mycurs.fetchall() #returns tuple with first row (unordered list)
        for line in a:
            run_id=line[0]
            for element in resultsList:
                if run_id==element.run_id and x==element.num_agents:
                    element.walkedD=line[1]
                    element.walkedDPercent=element.walkedD/40986771
                    #print(element.run_id, element.walkedD, element.walkedDPercent)


def allCrimes():
    for x in numagents:
        """select uniqueCrimes and cummCrimes"""
        mycurs.execute("""SELECT  run_id,
        COUNT(DISTINCT(object_id)),
        COUNT(object_id)
        FROM abm_res.res_la_roadsprototype f
        LEFT JOIN open.nyc_road_proj_final r
        ON r.gid=f.road_id
        LEFT JOIN open.nyc_road2pi_5ft_2015_jun p
        ON f.road_id=p.road_id
        WHERE NOT f.road_id is NULL AND agent<{0} AND {1}
        group by run_id""".format(x, select_ids))
        a=mycurs.fetchall() #returns tuple with first row (unordered list)
        print("current numagents: {}".format(x,select_ids))
        for line in a:
            run_id=line[0]
            for element in resultsList:
                if run_id==element.run_id and x==element.num_agents:
                    element.uniqueCrimes=line[1]
                    element.PercentuniqueCrimes=line[1]/crimesTotal
                    element.cummCrimes=line[2]
                    #print(element.run_id, element.uniqueCrimes, element.cummCrimes, element.num_agents)

def typesCrimes():
    crimetypes=["'BURGLARY'", "'ROBBERY'", "'GRAND LARCENY'", "'GRAND LARCENY OF MOTOR VEHICLE'", "'FELONY ASSAULT'"]
    for crimetype in crimetypes:
        for x in numagents:
            """select uniqueCrimes and cummCrimes"""
            mycurs.execute("""SELECT  run_id,
            COUNT(DISTINCT(object_id)),
            COUNT(object_id)
            FROM abm_res.res_la_roadsprototype f
            LEFT JOIN open.nyc_road_proj_final r
            ON r.gid=f.road_id
            LEFT JOIN open.nyc_road2pi_5ft_2015_jun p
            ON f.road_id=p.road_id
            WHERE NOT f.road_id is NULL AND agent<{0} AND offense={1} AND {2}
            group by run_id""".format(x, crimetype, select_ids))
            a=mycurs.fetchall() #returns tuple with first row (unordered list)
            for line in a:
                run_id=line[0]
                for element in resultsList:
                    if run_id==element.run_id and x==element.num_agents:
                        if crimetype=="'BURGLARY'":
                            element.BurglaryUniq=line[1]
                            element.PercentBurglaryUniq=line[1]/burglaryTotal
                            print(line)
                            print(element.PercentBurglaryUniq)
                            print(burglaryTotal)
                            element.BurglaryCumm=line[2]
                        if crimetype=="'ROBBERY'":
                            element.RobberyUniq=line[1]
                            element.PercentRobberyUniq=line[1]/robberyTotal
                            element.RobberyCumm=line[2]
                        if crimetype=="'GRAND LARCENY'":
                            element.LarcenyUniq=line[1]
                            element.PercentLarcenyUniq=line[1]/larcenyTotal
                            element.LarcenyCumm=line[2]
                        if crimetype=="'GRAND LARCENY OF MOTOR VEHICLE'":
                            element.LarcenyMotorUnique=line[1]
                            element.PercentLarcenyMotorUnique=line[1]/larcenyMTotal
                            element.LarcenyMotorCumm=line[2]
                        if crimetype=="'FELONY ASSAULT'": 
                            element.AssaultUnique=line[1]
                            element.PercentAssaultUnique=line[1]/assaultTotal
                            element.AssaultCumm=line[2]
                    #print(element.run_id, element.BurglaryUniq, element.LarcenyUniq, element.num_agents)


def calculatePAI():
    for element in resultsList:
        element.uniqPai=float(element.PercentuniqueCrimes)/float(element.walkedDPercent)
        print(element.uniqPai)
        element.uniquePaiBurglary=float(element.PercentBurglaryUniq)/float(element.walkedDPercent)
        element.uniquePaiRobbery=float(element.PercentRobberyUniq)/float(element.walkedDPercent)
        element.uniquePaiLarceny=float(element.PercentBurglaryUniq)/float(element.walkedDPercent)
        element.uniquePaiLarcneyM=float(element.PercentLarcenyMotorUnique)/float(element.walkedDPercent)
        element.uniquePaiAssault=float(element.PercentAssaultUnique)/float(element.walkedDPercent)


def createNewTable():
    try:
        mycurs.execute("""DROP TABLE {0}""".format(table))
    except:
        print("table does not exist yet")
    mycurs.execute("""CREATE TABLE {0} (
    run_id integer,
    num_agents numeric,
    totalnumagents numeric,
    "distancetype" varchar,
    "targettype" varchar,
    "wayfindingType" varchar,
    uniqueCrimes numeric,
    BurglaryUniq numeric,
    RobberyUniq numeric,
    LarcenyUniq numeric,
    LarcenyMotorUnique numeric,
    AssaultUnique numeric,

    cummCrimes numeric,
    BurglaryCumm numeric,
    RobberyCumm numeric,
    LarcenyCumm numeric,
    LarcenyMotorCumm numeric,
    AssaultCumm numeric,

    PercentuniqueCrimes numeric,
    PercentBurglaryUniq numeric,
    PercentRobberyUniq numeric,
    PercentLarcenyUniq numeric,
    PercentLarcenyMotorUnique numeric,
    PercentAssaultUnique numeric,

    uniqPai numeric,
    uniquePaiBurglary numeric,
    uniquePaiRobbery numeric,
    uniquePaiLarceny numeric,
    uniquePaiLarcneyM numeric,
    uniquePaiAssault numeric,
    walkedD numeric,
    walkedDPercent numeric)""".format(table))
    conn.commit()
    print("table created")

def insertValuesInTable():
    try:        
        for element in resultsList:
            mycurs.execute("""Insert into {0} ("run_id", "num_agents", "totalnumagents",
            "distancetype", "targettype", "wayfindingType", uniqueCrimes, BurglaryUniq, RobberyUniq, LarcenyUniq,
            LarcenyMotorUnique, AssaultUnique, cummCrimes, BurglaryCumm, RobberyCumm, LarcenyCumm,
            LarcenyMotorCumm, AssaultCumm, PercentuniqueCrimes, PercentBurglaryUniq, PercentRobberyUniq,
            PercentLarcenyUniq, PercentLarcenyMotorUnique, PercentAssaultUnique, uniqPai, uniquePaiBurglary,
            uniquePaiRobbery, uniquePaiLarceny, uniquePaiLarcneyM, uniquePaiAssault, walkedD, walkedDPercent
            ) values
            ({1},{2},{3},'{4}','{5}','{6}',{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},{23},{24},{25},{26},{27},{28},{29},{30},{31},{32})""".format(
            table,             
            element.run_id, element.num_agents, element.totalnumagents, str(element.distanceType), str(element.targetType), str(element.wayfindingType),
            element.uniqueCrimes, element.BurglaryUniq, element.RobberyUniq, element.LarcenyUniq, 
            element.LarcenyMotorUnique, element.AssaultUnique, element.cummCrimes, element.BurglaryCumm, element.RobberyCumm,
            element.LarcenyCumm, element.LarcenyMotorCumm, element.AssaultCumm, element.PercentuniqueCrimes, element.PercentBurglaryUniq,
            element.PercentRobberyUniq, element.PercentLarcenyUniq, element.PercentLarcenyMotorUnique, element.PercentAssaultUnique,
            element.uniqPai, element.uniquePaiBurglary, element.uniquePaiRobbery, element.uniquePaiLarceny, element.uniquePaiLarcneyM,
            element.uniquePaiAssault, element.walkedD, element.walkedDPercent))
            conn.commit()
    except:
        print("could not insert values in table ")
    conn.commit()
    conn.close()

conn= psycopg2.connect("dbname='shared' user='rraquel' host='127.0.0.1' password='Mobil4b' ")        
mycurs = conn.cursor()

numagents=[5, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000]
#for test
#numagents=[5]

table='abm_res.res_la_results1000agent'
#select_ids='(run_id=628 OR run_id=630)'
select_ids='(run_id>669 and run_id<689)'

#for test
#select_ids='run_id=620 OR run_id=62'

#mapped crimes for June 2015
crimesTotal=8494
burglaryTotal=1287
robberyTotal=1301
larcenyTotal=3555
larcenyMTotal=580
assaultTotal=1778

resultsList=[]
configdict={}
allcrimesdict={}
buildbase()
distance()
allCrimes()
typesCrimes()
calculatePAI()
#createNewTable()
insertValuesInTable()

print("inserted")

