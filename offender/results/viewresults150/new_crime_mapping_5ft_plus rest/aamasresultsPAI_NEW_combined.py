 import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections


conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
mycurs = conn.cursor()


"""===========plot target type and radius type per UNIQUE PAI========="""

def uniquePaiCrimesBest():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """combines best target type strategies per radius search"""

    mycurs.execute("""SELECT r."targettype",uniqPai, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents5 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=results

    mycurs.execute("""SELECT r."targettype",uniqPai, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents25 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",uniqPai, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents50 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",uniqPai, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents75 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",uniqPai, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents100 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",uniqPai, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents125 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results

    mycurs.execute("""SELECT r."targettype",uniqPai, m.num_agents, m.run_id
        FROM open.nyc_res_la_NEW_computenumagents150 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    resultstotal=resultstotal+results
    
    res=collections.defaultdict(list)
    print('best combineds')
    #each row is a run_id
    for row in resultstotal:
        targettype=row[0]
        print(targettype)
        uniquePai=float(row[1])
        agents=row[2]
        print(agents)
        runid=row[3]
        x=[uniquePai, agents]
        res[targettype].append(x)
        print(res)



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
    plot4=plt.plot(xrvc, yrvc, label='static distance - randomVenueCenter target')
    plot6=plt.plot(xpvc, ypvc, label='uniform distance - popularVenueCenter target')
    plot5=plt.plot(xpv, ypv, label='Lévy flight distance - popularVenue target')
    plt.axis([25,150,1,1.8])
    plt.xticks([25,50, 75,100,125,150])
    #ax.set_title('adapted PAI - comparing best performing scenarios')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('adapted PAI')
    plt.legend()
    plt.show()


uniquePaiCrimesBest()
