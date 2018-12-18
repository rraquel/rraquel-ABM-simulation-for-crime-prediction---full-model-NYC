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
        AND PercentuniqueCrimes>0.95 ORDER BY PercentuniqueCrimes ASC LIMIT 1""".format(run_id))
        results=mycurs.fetchall() #returns tuple wi
        for line in results:
            
            print("{0}, {1}, {2}, {3}".format(run_id, line[2], line[1], line[0]))



#distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract', 'taxiTractD', 'crimeTractM', 'crimeTractMD', 'crimeTract1x12', 'crimeTract1x12D', 'crimeTract1x6', 'crimeTract1']
distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract', 'crimeTractMD']
#distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract']
#distancetype=['crimeTract1x12D']
destinationType=['randomRoad', 'randomVenue', 'randomVenueCenter', 'randomVenueType', 'popularVenue', 'popularVenueCenter', 'popularVenueType']
uniquePaiCrimes()
#percent()
run_ids=[620, 625, 664, 633, 739]
#percentBest()