import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections


conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
mycurs = conn.cursor()


"""===========plot target type and radius type per UNIQUE PAI========="""

def uniquePercentCrimes():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents5 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='randomVenueCenter' AND "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents25 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='randomVenueCenter' AND "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents50 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='randomVenueCenter' AND  "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents75 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='randomVenueCenter' AND  "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents100 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='randomVenueCenter' AND  "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents125 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='randomVenueCenter' AND  "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents150 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='randomVenueCenter' AND  "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents5 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenueCenter' AND "radiustype"='uniformR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results
    print(results)

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents25 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenueCenter' AND "radiustype"='uniformR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents50 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenueCenter' AND  "radiustype"='uniformR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents75 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenueCenter' AND  "radiustype"='uniformR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results
    
    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents100 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenueCenter' AND  "radiustype"='uniformR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents125 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenueCenter' AND  "radiustype"='uniformR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents150 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenueCenter' AND  "radiustype"='uniformR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results


    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents5 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenue' AND "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents25 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenue' AND "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents50 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenue' AND  "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents75 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenue' AND  "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents100 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenue' AND  "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents125 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenue' AND  "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents150 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE "targettype"='popularVenue' AND  "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results
    print(resultstotal)

    res=collections.defaultdict(list)
    #each row is a run_id
    for row in resultstotal:
        targettype=row[0]
        print(targettype)
        uniquePercent=float(row[1])*100
        agents=row[2]
        print(agents)
        runid=row[3]
        x=[uniquePercent, agents]
        res[targettype].append(x)
        #print(res)


    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    yrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    xrr=np.array([np.array(xi) for xi in rr1])

    #"""randomRoadCenter"""
    #rrc0=[x[0] for x in res['randomRoadCenter']]
    #yrrc=np.array([np.array(xi) for xi in rrc0])
    #rrc1=[x[1] for x in res['randomRoadCenter']]
    #xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    yrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    xrv=np.array([np.array(xi) for xi in rv1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    yrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    xrvc=np.array([np.array(xi) for xi in rvc1])

    """popularVenue"""
    pv0=[x[0] for x in res['popularVenue']]
    ypv=np.array([np.array(xi) for xi in pv0])
    pv1=[x[1] for x in res['popularVenue']]
    xpv=np.array([np.array(xi) for xi in pv1])

    """popularVenueCenter"""
    pvc0=[x[0] for x in res['popularVenueCenter']]
    ypvc=np.array([np.array(xi) for xi in pvc0])
    pvc1=[x[1] for x in res['popularVenueCenter']]
    xpvc=np.array([np.array(xi) for xi in pvc1])

    fig=plt.figure(1)
    ax=plt.subplot(111)
    #plot1=plt.plot(xrr, yrr, label='RandomRoad')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    #plot3=plt.plot(xrv, yrv, label='randomVenue')
    plot4=plt.plot(xrvc, yrvc, label='static distance - randomVenueCenter target')
    plot5=plt.plot(xpv, ypv, label='Lévy flight distance - popularVenue target')
    plot6=plt.plot(xpvc, ypvc, label='uniform distance - popularVenueCenter target')
    plt.axis([25,150,0,100])
    plt.xticks([25,50, 75,100,125,150])
    #ax.set_title('Percent covered unique crimes - Lévy distance')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('% coverage unique crimes')
    plt.legend()
    plt.show()




uniquePercentCrimes()
