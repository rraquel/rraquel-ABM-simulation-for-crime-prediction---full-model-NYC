import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections
from scipy.integrate import simps
from numpy import trapz


conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")   
mycurs = conn.cursor()


def buildCases(results, type, dt):

    res=collections.defaultdict(list)
    #each row is a run_id
    if type==0:
        for row in results:
            targettype=row[0]
            #print(targettype)
            uniquePai=float(row[1])
            #print(uniquePai)
            agents=row[2]
            #print(agents)
            runid=row[3]
            x=[uniquePai, agents]
            res[targettype].append(x)
            #print(res)
    elif type==1:
        for row in results:
            targettype=row[0]
            #print(targettype)
            uniquePercent=float(row[1])*100
            agents=row[2]
            #print(agents)
            runid=row[3]
            x=[uniquePercent, agents]
            res[targettype].append(x)
            ##print(res)
    
 
    n=[5, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000]

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]    
    area = trapz(rr0,n, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area yrr=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(rr0,n, dx=5)
    #print("area yrr=", area)

    #"""randomRoadCenter"""

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    area = trapz(rv0, n, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area yrv=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(rv0,n, dx=5)
    #print("area yrv=", area)

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    area = trapz(rvc0,n, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area yrvc=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(rvc0,n, dx=5)
    #print("area yrvc=", area)

    """randomVenueType"""
    rvc0=[x[0] for x in res['randomVenueType']]
    area = trapz(rvc0, n, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area yrvt=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(rvc0, n, dx=5)
    #print("area yrvt=", area)

    """popularVenue"""
    pv0=[x[0] for x in res['popularVenue']]
    area = trapz(pv0, n, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area ypv=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(pv0, n, dx=5)
    #print("area ypv=", area)

    """popularVenueCenter"""
    pvc0=[x[0] for x in res['popularVenueCenter']]
    area = trapz(pvc0, n, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area ypvc=")
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(pvc0, n, dx=5)
    #print("area ypvc=", area)

    """popularVenueType"""
    pvc0=[x[0] for x in res['popularVenueType']]
    area = trapz(pvc0, n, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area ypvt=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(pvc0, n, dx=5)
    #print("area ypvt=", area)


################################################################################################################################################################## 

"""===========plot target type and radius type per UNIQUE PAI========="""

def uniquePaiCrimes():
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""
    for dt in distancetype:
        mycurs.execute("""SELECT "targettype",uniqPai, num_agents, run_id
        FROM abm_res.res_la_results1000agent AS m
        WHERE "distancetype"='{0}'""".format(dt))
        results=mycurs.fetchall() #returns tuple with first row (unordered list)
        #print(results)
        print(dt)
        buildCases(results, 0, dt)

def percent():
    for dt in distancetype:
        for dest in destinationType:
            mycurs.execute("""SELECT PercentuniqueCrimes, uniqPai, num_agents, run_id
            FROM abm_res.res_la_results1000agent AS m
            WHERE "distancetype"='{0}' AND "targettype"='{1}'
            AND PercentuniqueCrimes>0.85 ORDER BY PercentuniqueCrimes ASC LIMIT 1""".format(dt, dest))
            results=mycurs.fetchall() #returns tuple wi
            for line in results:
                #print(dt)
                print("{0}, {1}, {2}, {3}".format(dest, line[2], line[1], line[0]))

def percentBest():
    for run_id in run_ids:
        #÷print(run_id)
        mycurs.execute("""SELECT PercentuniqueCrimes, uniqPai, num_agents, run_id
        FROM abm_res.res_la_results1000agent AS m
        WHERE run_id={}
        AND PercentuniqueCrimes>0.20 ORDER BY PercentuniqueCrimes ASC LIMIT 1""".format(run_id))
        results=mycurs.fetchall() #returns tuple wi
        for line in results:
            
            print("{0}, {1}, {2}, {3}".format(run_id, line[2], line[1], line[0]))


################################################################################################################################################################## 

def auccrimetypes(runid):
    mycurs.execute("""SELECT "targettype",uniquePaiBurglary,
        uniquePaiRobbery, uniquepailarceny, uniquePaiLarcneyM,
        uniquePaiAssault, num_agents, run_id, uniqPai
        FROM abm_res.res_la_results1000agent
        where run_id={}""".format(runid))
    result = mycurs.fetchall()  # returns tuple with first row (unordered list)
    res2=collections.defaultdict(list)
    for row in result:
        runid = row[7]
        targettype = row[0]
        uniquePaiB = float(row[1])
        uniquePaiR = float(row[2])
        uniquePaiL = float(row[3])
        uniquePaiLM = float(row[4])
        uniquePaiA = float(row[5])
        uniqPai=float(row[8])
        agents = row[6]
        runid = row[7]
        b = [uniquePaiB, agents]
        crimetype = 'b'
        res2[crimetype].append(b)
        r = [uniquePaiR, agents]
        crimetype = 'r'
        res2[crimetype].append(r)
        l = [uniquePaiL, agents]
        crimetype = 'l'
        res2[crimetype].append(l)
        m = [uniquePaiLM, agents]
        crimetype = 'm'
        res2[crimetype].append(m)
        a = [uniquePaiA, agents]
        crimetype = 'a'
        res2[crimetype].append(a)
        c = [uniqPai, agents]
        crimetype = 'c'
        res2[crimetype].append(c)

    n=[5, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000]

    rr0 = [x[0] for x in res2['b']]
    area = trapz(rr0, n, dx=5)
    print(area)

    rrc0 = [x[0] for x in res2['r']]
    area = trapz(rrc0, n, dx=5)
    print(area)

    rv0 = [x[0] for x in res2['l']]
    area = trapz(rv0, n, dx=5)
    print(area)

    rvc0 = [x[0] for x in res2['m']]
    area = trapz(rvc0, n, dx=5)
    print(area)

    pv0 = [x[0] for x in res2['a']]
    area = trapz(pv0, n, dx=5)
    print(area)

    pv2 = [x[0] for x in res2['c']]
    area = trapz(pv2, n, dx=5)
    print(area)

def percentBestcrimes():
    for run_id in run_ids:
        crimes=[('PercentuniqueCrimes', 'uniqPai'), ('percentburglaryuniq', 'uniquepaiburglary'), ('percentrobberyuniq', 'uniquepairobbery'), ('percentlarcenyuniq', 'uniquepailarceny'), ('percentlarcenymotorunique', 'uniquepailarcneym'), ('percentassaultunique', 'uniquepaiassault')]
        for crime in crimes:
            #÷print(run_id)
            mycurs.execute("""SELECT {0}, {1}, num_agents, run_id
            FROM abm_res.res_la_results1000agent AS m
            WHERE run_id={2}
            AND {3}>0.80 ORDER BY {4} ASC LIMIT 1""".format(crime[0],crime[1], run_id, crime[0], crime[0]))
            results=mycurs.fetchall() #returns tuple wi
            for line in results:
                #print run_id, num agents, pai an dpercent
                print("{0}, {1}, {2}, {3}, {4}".format(run_id, line[2], line[1], line[0], crime[0]))
        

################################################################################################################################################################## 



#distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract', 'taxiTractD', 'crimeTractM', 'crimeTractMD', 'crimeTract1x12', 'crimeTract1x12D', 'crimeTract1x6', 'crimeTract1']
distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract', 'crimeTractMD']
#distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract']
#distancetype=['crimeTract1x12D']
destinationType=['randomRoad', 'randomVenue', 'randomVenueCenter', 'randomVenueType', 'popularVenue', 'popularVenueCenter', 'popularVenueType']
#uniquePaiCrimes()
#percent()
run_ids=[620, 625, 664, 633, 739]
#percentBest()
#beset best 633 739
#auccrimetypes(633)
run_ids=[633, 739]
percentBestcrimes()