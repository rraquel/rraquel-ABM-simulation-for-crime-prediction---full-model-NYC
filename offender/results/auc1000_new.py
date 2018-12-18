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
    
 
    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    yrr=np.array([np.array(xi) for xi in rr0])
    area = trapz(yrr, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area yrr=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(yrr, dx=5)
    #print("area yrr=", area)

    #"""randomRoadCenter"""
    #rrc0=[x[0] for x in res['randomRoadCenter']]
    #yrrc=np.array([np.array(xi) for xi in rrc0])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    yrv=np.array([np.array(xi) for xi in rv0])
    area = trapz(yrv, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area yrv=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(yrv, dx=5)
    #print("area yrv=", area)

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    yrvc=np.array([np.array(xi) for xi in rvc0])
    area = trapz(yrvc, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area yrvc=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(yrvc, dx=5)
    #print("area yrvc=", area)

    """randomVenueType"""
    rvc0=[x[0] for x in res['randomVenueType']]
    yrvt=np.array([np.array(xi) for xi in rvc0])
    area = trapz(yrvt, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area yrvt=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(yrvt, dx=5)
    #print("area yrvt=", area)

    """popularVenue"""
    pv0=[x[0] for x in res['popularVenue']]
    ypv=np.array([np.array(xi) for xi in pv0])
    area = trapz(ypv, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area ypv=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(ypv, dx=5)
    #print("area ypv=", area)

    """popularVenueCenter"""
    pvc0=[x[0] for x in res['popularVenueCenter']]
    ypvc=np.array([np.array(xi) for xi in pvc0])
    area = trapz(ypvc, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area ypvc=")
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(ypvc, dx=5)
    #print("area ypvc=", area)

    """popularVenueType"""
    pvc0=[x[0] for x in res['popularVenueType']]
    ypvt=np.array([np.array(xi) for xi in pvc0])
    area = trapz(ypvt, dx=5)
    # Compute the area using the composite trapezoidal rule.
    #print("area ypvt=", area)
    print(area)
    # Compute the area using the composite Simpson's rule.
    area = simps(ypvt, dx=5)
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
            AND PercentuniqueCrimes>0.9 ORDER BY PercentuniqueCrimes ASC LIMIT 1""".format(dt, dest))
            results=mycurs.fetchall() #returns tuple wi
            for line in results:
                #print(dt)
                print("{0}, {1}, {2}, {3}".format(dest, line[2], line[1], line[0]))



#distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract', 'taxiTractD', 'crimeTractM', 'crimeTractMD', 'crimeTract1x12', 'crimeTract1x12D', 'crimeTract1x6', 'crimeTract1']
distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract', 'crimeTractMD']
#distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract']
destinationType=['randomRoad', 'randomVenue', 'randomVenueCenter', 'randomVenueType', 'popularVenue', 'popularVenueCenter', 'popularVenueType']
#uniquePaiCrimes()
percent()