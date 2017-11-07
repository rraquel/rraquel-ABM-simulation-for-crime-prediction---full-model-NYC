import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections


conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
mycurs = conn.cursor()

"""===========plot num agents vs hit rate (uniqueCrimes/total)========="""

def hitCrimes():
    """----------ALL CRIMES----------"""
    mycurs.execute("""SELECT "targettype", "PercentuniqueCrimes", num_agents FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and radiustype='uniformR' """)
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    res=collections.defaultdict(list)

    for row in results:
        targettype=row[0]
        x1=row[1]
        x2=row[2]
        x=[x1,x2]
        res[targettype].append(x)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    yrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    xrr=np.array([np.array(xi) for xi in rr1])

    """randomRoadCenter"""
    rrc0=[x[0] for x in res['randomRoadCenter']]
    yrrc=np.array([np.array(xi) for xi in rrc0])
    rrc1=[x[1] for x in res['randomRoadCenter']]
    xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    yrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    xrvc=np.array([np.array(xi) for xi in rvc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    yrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    xrv=np.array([np.array(xi) for xi in rv1])

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

    plt.figure(1)
    plt.subplot(211)
    plot1=plt.plot(xrr, yrr,'ko')
    plot2=plt.plot(xrrc, yrrc, 'ks')
    plot3=plt.plot(xrvc, yrvc, 'k*')
    plot4=plt.plot(xrv, yrv, 'kp')
    plot5=plt.plot(xpv, ypv, 'kP')
    plot6=plt.plot(xpvc, ypvc, 'kv')
    plt.axis([0,200,0.1,0.5])
    #plt.legend([plot1, plot2, plot3, plot4, plot4, plot5, plot6], ('randomRoad','randomRoadCenter', 'randomVenueCenter', 'randomVenue', 'popularVenue', 'popularVenueCenter'),'best' numpoints=1)
    patch1 = mpatches.Patch(color='red', label='randomroad')
    patch2 = mpatches.Patch(color='blue', label='randomRoadCenter')
    patch3 = mpatches.Patch(color='yellow', label='randomVenueCenter')
    patch4 = mpatches.Patch(color='green', label='randomVenue')
    patch5 = mpatches.Patch(color='cyan', label='popularVenue')
    patch6 = mpatches.Patch(color='magenta', label='popularVenueCenter')
    plt.legend(handles=[patch1, patch2, patch3, patch4, patch5, patch6], bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.show()

def hitBurglary():
    """----------bURGLARY----------"""
    mycurs.execute("""SELECT "targettype", "PercentBurglaryUniq", num_agents FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and radiustype='uniformR' """)
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    res=collections.defaultdict(list)

    for row in results:
        targettype=row[0]
        x1=row[1]
        x2=row[2]
        x=[x1,x2]
        res[targettype].append(x)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    yrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    xrr=np.array([np.array(xi) for xi in rr1])

    """randomRoadCenter"""
    rrc0=[x[0] for x in res['randomRoadCenter']]
    yrrc=np.array([np.array(xi) for xi in rrc0])
    rrc1=[x[1] for x in res['randomRoadCenter']]
    xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    yrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    xrvc=np.array([np.array(xi) for xi in rvc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    yrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    xrv=np.array([np.array(xi) for xi in rv1])

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

    plt.figure(1)
    plt.subplot(211)
    plt.plot(xrr, yrr, '-ro')
    plt.plot(xrrc, yrrc, '-bo')
    plt.plot(xrvc, yrvc, '-yo')
    plt.plot(xrv, yrv, '-go')
    plt.plot(xpv, ypv, '-co')
    plt.plot(xpvc, ypvc, '-mo')
    plt.axis([0,200,0.1,0.5])
    #plt.plot(t12, t22, 'b-*')
    plt.show()

def hitRobbery():
    """----------ROBBERY----------"""
    mycurs.execute("""SELECT "targettype", "PercentRobberyUniq", num_agents FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and radiustype='uniformR' """)
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    res=collections.defaultdict(list)

    for row in results:
        targettype=row[0]
        x1=row[1]
        x2=row[2]
        x=[x1,x2]
        res[targettype].append(x)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    yrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    xrr=np.array([np.array(xi) for xi in rr1])

    """randomRoadCenter"""
    rrc0=[x[0] for x in res['randomRoadCenter']]
    yrrc=np.array([np.array(xi) for xi in rrc0])
    rrc1=[x[1] for x in res['randomRoadCenter']]
    xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    yrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    xrvc=np.array([np.array(xi) for xi in rvc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    yrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    xrv=np.array([np.array(xi) for xi in rv1])

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

    plt.figure(1)
    plt.subplot(211)
    plt.plot(xrr, yrr, '-ro')
    plt.plot(xrrc, yrrc, '-bo')
    plt.plot(xrvc, yrvc, '-yo')
    plt.plot(xrv, yrv, '-go')
    plt.plot(xpv, ypv, '-co')
    plt.plot(xpvc, ypvc, '-mo')
    plt.axis([0,200,0.1,0.5])
    #plt.plot(t12, t22, 'b-*')
    plt.show()


def hitLarceny():
    """----------LARCENY----------"""
    mycurs.execute("""SELECT "targettype", "PercentLarcenyUniq", num_agents FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and radiustype='uniformR' """)
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    res=collections.defaultdict(list)

    for row in results:
        targettype=row[0]
        x1=row[1]
        x2=row[2]
        x=[x1,x2]
        res[targettype].append(x)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    yrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    xrr=np.array([np.array(xi) for xi in rr1])

    """randomRoadCenter"""
    rrc0=[x[0] for x in res['randomRoadCenter']]
    yrrc=np.array([np.array(xi) for xi in rrc0])
    rrc1=[x[1] for x in res['randomRoadCenter']]
    xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    yrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    xrvc=np.array([np.array(xi) for xi in rvc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    yrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    xrv=np.array([np.array(xi) for xi in rv1])

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

    plt.figure(1)
    plt.subplot(211)
    plt.plot(xrr, yrr, '-ro')
    plt.plot(xrrc, yrrc, '-bo')
    plt.plot(xrvc, yrvc, '-yo')
    plt.plot(xrv, yrv, '-go')
    plt.plot(xpv, ypv, '-co')
    plt.plot(xpvc, ypvc, '-mo')
    plt.axis([0,200,0.1,0.5])
    #plt.plot(t12, t22, 'b-*')
    plt.show()

def hitLarcenyM():
    """----------LARCENY MOTOR----------"""
    mycurs.execute("""SELECT "targettype", "PercentLarcenyMotorUnique", num_agents FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and radiustype='uniformR' """)
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    res=collections.defaultdict(list)

    for row in results:
        targettype=row[0]
        x1=row[1]
        x2=row[2]
        x=[x1,x2]
        res[targettype].append(x)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    yrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    xrr=np.array([np.array(xi) for xi in rr1])

    """randomRoadCenter"""
    rrc0=[x[0] for x in res['randomRoadCenter']]
    yrrc=np.array([np.array(xi) for xi in rrc0])
    rrc1=[x[1] for x in res['randomRoadCenter']]
    xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    yrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    xrvc=np.array([np.array(xi) for xi in rvc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    yrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    xrv=np.array([np.array(xi) for xi in rv1])

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

    plt.figure(1)
    plt.subplot(211)
    plt.plot(xrr, yrr, '-ro')
    plt.plot(xrrc, yrrc, '-bo')
    plt.plot(xrvc, yrvc, '-yo')
    plt.plot(xrv, yrv, '-go')
    plt.plot(xpv, ypv, '-co')
    plt.plot(xpvc, ypvc, '-mo')
    plt.axis([0,200,0.1,0.5])
    #plt.plot(t12, t22, 'b-*')
    plt.show()

def hitAssault():
    """----------ASSALUT----------"""
    mycurs.execute("""SELECT "targettype", "PercentAssaultUnique", num_agents FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and radiustype='uniformR' """)
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    res=collections.defaultdict(list)

    for row in results:
        targettype=row[0]
        x1=row[1]
        x2=row[2]
        x=[x1,x2]
        res[targettype].append(x)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    yrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    xrr=np.array([np.array(xi) for xi in rr1])

    """randomRoadCenter"""
    rrc0=[x[0] for x in res['randomRoadCenter']]
    yrrc=np.array([np.array(xi) for xi in rrc0])
    rrc1=[x[1] for x in res['randomRoadCenter']]
    xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    yrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    xrvc=np.array([np.array(xi) for xi in rvc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    yrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    xrv=np.array([np.array(xi) for xi in rv1])

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

    plt.figure(1)
    plt.subplot(211)
    plt.plot(xrr, yrr, '-ro')
    plt.plot(xrrc, yrrc, '-bo')
    plt.plot(xrvc, yrvc, '-yo')
    plt.plot(xrv, yrv, '-go')
    plt.plot(xpv, ypv, '-co')
    plt.plot(xpvc, ypvc, '-mo')
    plt.axis([0,200,0.1,0.5])
    #plt.plot(t12, t22, 'b-*')
    plt.show()


    """===========plot target type and radius type per UNIQUE PAI========="""

def uniquePaiCrimesU():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""
    mycurs.execute("""SELECT "targettype","PercentuniqueCrimes", num_agents, r.run_id
    FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and (num_agents=150 OR num_agents=100) AND
    "targettype" is not null AND (start_date between '2017-11-02 13:51:20' and '2017-12-01')
    AND "radiustype"='uniformR'""")
    results100=mycurs.fetchall() #returns tuple with first row (unordered list)
    print(results100)

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents25 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='uniformR'""")
    results25=mycurs.fetchall() #returns tuple with first row (unordered list)

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents50 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='uniformR'""")
    results50=mycurs.fetchall() #returns tuple with first row (unordered list)

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents75 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='uniformR'""")
    results75=mycurs.fetchall() #returns tuple with first row (unordered list)

    results=results100+results75+results50+results25
    print(results[0])
    print(results)

    res=collections.defaultdict(list)
    print('UNIFORM')
    #each row is a run_id
    for row in results:
        targettype=row[0]
        print(targettype)
        percent=float(row[1])
        agents=row[2]
        print(agents)
        runid=row[3]
        totaldist=float(40986771)

        mycurs.execute("""select sum(shape_leng) from (
        select distinct(run.road_id), road.shape_leng from open.res_la_roads run
        LEFT JOIN open.nyc_road_proj_final as road on road.gid=run.road_id WHERE run_id={}) as x
        """.format(runid))
        uDistance=mycurs.fetchall()
        uDist=float(uDistance[0][0])

        uniquePai=(percent)/(uDist/40986771)
        print(uniquePai)
        x=[uniquePai, agents]
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
    plot1=plt.plot(xrr, yrr, label='RandomRoad')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    plot3=plt.plot(xrv, yrv, label='randomVenue')
    plot4=plt.plot(xrvc, yrvc, label='randomVenueCenter')
    plot5=plt.plot(xpv, ypv, label='popularVenue')
    plot6=plt.plot(xpvc, ypvc, label='popularVenueCenter')
    plt.axis([25,160,0,1])
    ax.set_title('Unique adapted PAI for all crime types over n of agents, for Uniform distributed search radius')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique crimes adapted PAI')
    plt.legend()
    plt.show()


def uniquePaiCrimesS():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""
    mycurs.execute("""SELECT "targettype","PercentuniqueCrimes", num_agents, r.run_id
    FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and (num_agents=150 OR num_agents=100) AND
    "targettype" is not null AND (start_date between '2017-11-02 13:51:20' and '2017-12-01')
    AND "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents25 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='staticR'""")
    results25=mycurs.fetchall() #returns tuple with first row (unordered list)

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents50 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='staticR'""")
    results50=mycurs.fetchall() #returns tuple with first row (unordered list)

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents75 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='staticR'""")
    results75=mycurs.fetchall() #returns tuple with first row (unordered list)

    results=results100+results75+results50+results25

    res=collections.defaultdict(list)
    print('STATIC')
    #each row is a run_id
    for row in results:
        targettype=row[0]
        print(targettype)
        percent=float(row[1])
        agents=row[2]
        print(agents)
        runid=row[3]
        totaldist=float(40986771)

        mycurs.execute("""select sum(shape_leng) from (
        select distinct(run.road_id), road.shape_leng from open.res_la_roads run
        LEFT JOIN open.nyc_road_proj_final as road on road.gid=run.road_id WHERE run_id={}) as x
        """.format(runid))
        uDistance=mycurs.fetchall()
        uDist=float(uDistance[0][0])

        uniquePai=(percent)/(uDist/40986771)
        print(uniquePai)
        x=[uniquePai, agents]
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
    plot1=plt.plot(xrr, yrr, label='RandomRoad')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    plot3=plt.plot(xrv, yrv, label='randomVenue')
    plot4=plt.plot(xrvc, yrvc, label='randomVenueCenter')
    plot5=plt.plot(xpv, ypv, label='popularVenue')
    plot6=plt.plot(xpvc, ypvc, label='popularVenueCenter')
    plt.axis([25,160,0,1])
    ax.set_title('Unique adapted PAI for all crime types over n of agents, for static search radius')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique crimes adapted PAI')
    plt.legend()
    plt.show()


def uniquePaiCrimesP():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""
    mycurs.execute("""SELECT "targettype","PercentuniqueCrimes", num_agents, r.run_id
        FROM open.res_la_model AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and step=29 and (num_agents=150 OR num_agents=100) AND
        "targettype" is not null AND (start_date between '2017-11-02 13:51:20' and '2017-12-01')
        AND "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents25 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='powerR'""")
    results25=mycurs.fetchall() #returns tuple with first row (unordered list)

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents50 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='powerR'""")
    results50=mycurs.fetchall() #returns tuple with first row (unordered list)

    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents75 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='powerR'""")
    results75=mycurs.fetchall() #returns tuple with first row (unordered list)

    results=results100+results75+results50+results25

    res=collections.defaultdict(list)
    print('POWER')
    #each row is a run_id
    for row in results:
        targettype=row[0]
        print(targettype)
        percent=float(row[1])
        agents=row[2]
        print(agents)
        runid=row[3]
        totaldist=float(40986771)

        mycurs.execute("""select sum(shape_leng) from (
        select distinct(run.road_id), road.shape_leng from open.res_la_roads run
        LEFT JOIN open.nyc_road_proj_final as road on road.gid=run.road_id WHERE run_id={}) as x
        """.format(runid))
        uDistance=mycurs.fetchall()
        uDist=float(uDistance[0][0])

        uniquePai=(percent)/(uDist/40986771)
        print(uniquePai)
        x=[uniquePai, agents]
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
    plot1=plt.plot(xrr, yrr, label='RandomRoad')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    plot3=plt.plot(xrv, yrv, label='randomVenue')
    plot4=plt.plot(xrvc, yrvc, label='randomVenueCenter')
    plot5=plt.plot(xpv, ypv, label='popularVenue')
    plot6=plt.plot(xpvc, ypvc, label='popularVenueCenter')
    plt.axis([25,160,0,1])
    ax.set_title('Unique adapted PAI for all crime types over n of agents, for power-law disrtributed search radius')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique crimes adapted PAI')
    plt.legend()
    plt.show()



 #not readable in the graph   
def uniquePaiCrimes():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""
    mycurs.execute("""SELECT "targettype","PercentuniqueCrimes", num_agents, r.run_id
    FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and "targettype" is not null AND (start_date between '2017-11-02 13:51:20' and '2017-12-01') AND "radiustype"='uniformR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    res=collections.defaultdict(list)

    #each row is a run_id
    for row in results:
        print('STATIC')
        targettype=row[0]
        print(targettype)
        percent=float(row[1])
        agents=row[2]
        print(agents)
        runid=row[3]
        totaldist=float(40986771)

        mycurs.execute("""select sum(shape_leng) from (
        select distinct(run.road_id), road.shape_leng from open.res_la_roads run
        LEFT JOIN open.nyc_road_proj_final as road on road.gid=run.road_id WHERE run_id={}) as x
        """.format(runid))
        uDistance=mycurs.fetchall()
        uDist=float(uDistance[0][0])

        uniquePai=(percent)/(uDist/40986771)
        print(uniquePai)
        x=[uniquePai, agents]
        res[targettype].append(x)
        #print(res)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    ayrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    axrr=np.array([np.array(xi) for xi in rr1])

    #"""randomRoadCenter"""
    #rrc0=[x[0] for x in res['randomRoadCenter']]
    #yrrc=np.array([np.array(xi) for xi in rrc0])
    #rrc1=[x[1] for x in res['randomRoadCenter']]
    #xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    ayrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    axrv=np.array([np.array(xi) for xi in rv1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    ayrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    axrvc=np.array([np.array(xi) for xi in rvc1])

    """popularVenue"""
    pv0=[x[0] for x in res['popularVenue']]
    aypv=np.array([np.array(xi) for xi in pv0])
    pv1=[x[1] for x in res['popularVenue']]
    axpv=np.array([np.array(xi) for xi in pv1])

    """popularVenueCenter"""
    pvc0=[x[0] for x in res['popularVenueCenter']]
    aypvc=np.array([np.array(xi) for xi in pvc0])
    pvc1=[x[1] for x in res['popularVenueCenter']]
    axpvc=np.array([np.array(xi) for xi in pvc1])




    """distinct crimes and distinct roads"""
    mycurs.execute("""SELECT "targettype","PercentuniqueCrimes", num_agents, r.run_id
    FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and "targettype" is not null AND (start_date between '2017-11-02 13:51:20' and '2017-12-01') AND "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    res=collections.defaultdict(list)

    #each row is a run_id
    for row in results:
        print('UNIFORM')
        targettype=row[0]
        print(targettype)
        percent=float(row[1])
        agents=row[2]
        print(agents)
        runid=row[3]
        totaldist=float(40986771)

        mycurs.execute("""select sum(shape_leng) from (
        select distinct(run.road_id), road.shape_leng from open.res_la_roads run
        LEFT JOIN open.nyc_road_proj_final as road on road.gid=run.road_id WHERE run_id={}) as x
        """.format(runid))
        uDistance=mycurs.fetchall()
        uDist=float(uDistance[0][0])

        uniquePai=(percent)/(uDist/40986771)
        print(uniquePai)
        x=[uniquePai, agents]
        res[targettype].append(x)
        #print(res)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    byrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    bxrr=np.array([np.array(xi) for xi in rr1])

    #"""randomRoadCenter"""
    #rrc0=[x[0] for x in res['randomRoadCenter']]
    #yrrc=np.array([np.array(xi) for xi in rrc0])
    #rrc1=[x[1] for x in res['randomRoadCenter']]
    #xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    byrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    bxrv=np.array([np.array(xi) for xi in rv1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    byrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    bxrvc=np.array([np.array(xi) for xi in rvc1])

    """popularVenue"""
    pv0=[x[0] for x in res['popularVenue']]
    bypv=np.array([np.array(xi) for xi in pv0])
    pv1=[x[1] for x in res['popularVenue']]
    bxpv=np.array([np.array(xi) for xi in pv1])

    """popularVenueCenter"""
    pvc0=[x[0] for x in res['popularVenueCenter']]
    bypvc=np.array([np.array(xi) for xi in pvc0])
    pvc1=[x[1] for x in res['popularVenueCenter']]
    bxpvc=np.array([np.array(xi) for xi in pvc1])


    
    """distinct crimes and distinct roads"""
    mycurs.execute("""SELECT "targettype","PercentuniqueCrimes", num_agents, r.run_id
    FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and "targettype" is not null AND (start_date between '2017-11-02 13:51:20' and '2017-12-01') AND "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    res=collections.defaultdict(list)

    #each row is a run_id
    for row in results:
        print('POWER')
        targettype=row[0]
        print(targettype)
        percent=float(row[1])
        agents=row[2]
        print(agents)
        runid=row[3]
        totaldist=float(40986771)

        mycurs.execute("""select sum(shape_leng) from (
        select distinct(run.road_id), road.shape_leng from open.res_la_roads run
        LEFT JOIN open.nyc_road_proj_final as road on road.gid=run.road_id WHERE run_id={}) as x
        """.format(runid))
        uDistance=mycurs.fetchall()
        uDist=float(uDistance[0][0])

        uniquePai=(percent)/(uDist/40986771)
        print(uniquePai)
        x=[uniquePai, agents]
        res[targettype].append(x)
        #print(res)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    cyrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    cxrr=np.array([np.array(xi) for xi in rr1])

    #"""randomRoadCenter"""
    #rrc0=[x[0] for x in res['randomRoadCenter']]
    #yrrc=np.array([np.array(xi) for xi in rrc0])
    #rrc1=[x[1] for x in res['randomRoadCenter']]
    #xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    cyrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    cxrv=np.array([np.array(xi) for xi in rv1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    cyrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    cxrvc=np.array([np.array(xi) for xi in rvc1])

    """popularVenue"""
    pv0=[x[0] for x in res['popularVenue']]
    cypv=np.array([np.array(xi) for xi in pv0])
    pv1=[x[1] for x in res['popularVenue']]
    cxpv=np.array([np.array(xi) for xi in pv1])

    """popularVenueCenter"""
    cvc0=[x[0] for x in res['popularVenueCenter']]
    cypvc=np.array([np.array(xi) for xi in pvc0])
    cvc1=[x[1] for x in res['popularVenueCenter']]
    cxpvc=np.array([np.array(xi) for xi in pvc1])

    fig=plt.figure(1)
    ax=plt.subplot(111)

    plot1=plt.plot(axrr, ayrr, label='RandomRoad-U')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    plot3=plt.plot(axrv, ayrv, label='randomVenue-U')
    plot4=plt.plot(axrvc, ayrvc, label='randomVenueCenter-U')
    plot5=plt.plot(axpv, aypv, label='popularVenue-U')
    plot6=plt.plot(axpvc, aypvc, label='popularVenueCenter-U')

    plot1b=plt.plot(bxrr, byrr, label='RandomRoad-S')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    plot3b=plt.plot(bxrv, byrv, label='randomVenue-S')
    plot4b=plt.plot(bxrvc, byrvc, label='randomVenueCenter-S')
    plot5b=plt.plot(bxpv, bypv, label='popularVenue-S')
    plot6b=plt.plot(bxpvc, bypvc, label='popularVenueCenter-S')
    plt.axis([25,160,0,1])

    plot1c=plt.plot(cxrr, cyrr, label='RandomRoad-P')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    plot3c=plt.plot(cxrv, cyrv, label='randomVenue-P') 
    plot4c=plt.plot(cxrvc, cyrvc, label='randomVenueCenter-P')
    plot5c=plt.plot(cxpv, cypv, label='popularVenue-U')
    plot6c=plt.plot(cxpvc, cypvc, label='popularVenueCenter-P')

    ax.set_title('Unique adapted PAI for all crime types over n of agents')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique crimes adapted PAI')
    plt.legend()
    plt.show()


def uniquePaiBurglary():

    """----------ALL BURGLARY---------"""
    """distinct crimes and distinct roads"""
    mycurs.execute("""SELECT "targettype","PercentBurglaryUniq", num_agents, r.run_id
    FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and (num_agents=100 or num_agents=150) and "targettype" is not null AND (start_date between '2017-11-02 13:51:20' and '2017-12-01') AND "radiustype"='uniformR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    mycurs.execute("""SELECT r."targettype",PercentBurglaryUniq, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents25 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='uniformR'""")
    results25=mycurs.fetchall() #returns tuple with first row (unordered list)

    mycurs.execute("""SELECT r."targettype",PercentBurglaryUniq, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents50 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='uniformR'""")
    results50=mycurs.fetchall() #returns tuple with first row (unordered list)

    res=collections.defaultdict(list)

    #each row is a run_id
    for row in results:
        print('STATIC')
        targettype=row[0]
        print(targettype)
        percent=float(row[1])
        agents=row[2]
        print(agents)
        runid=row[3]
        totaldist=float(40986771)

        mycurs.execute("""select sum(shape_leng) from (
        select distinct(run.road_id), road.shape_leng from open.res_la_roads run
        LEFT JOIN open.nyc_road_proj_final as road on road.gid=run.road_id WHERE run_id={}) as x
        """.format(runid))
        uDistance=mycurs.fetchall()
        uDist=float(uDistance[0][0])

        uniquePai=(percent)/(uDist/40986771)
        print(uniquePai)
        x=[uniquePai, agents]
        res[targettype].append(x)
        #print(res)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    ayrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    axrr=np.array([np.array(xi) for xi in rr1])

    #"""randomRoadCenter"""
    #rrc0=[x[0] for x in res['randomRoadCenter']]
    #yrrc=np.array([np.array(xi) for xi in rrc0])
    #rrc1=[x[1] for x in res['randomRoadCenter']]
    #xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    ayrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    axrv=np.array([np.array(xi) for xi in rv1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    ayrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    axrvc=np.array([np.array(xi) for xi in rvc1])

    """popularVenue"""
    pv0=[x[0] for x in res['popularVenue']]
    aypv=np.array([np.array(xi) for xi in pv0])
    pv1=[x[1] for x in res['popularVenue']]
    axpv=np.array([np.array(xi) for xi in pv1])

    """popularVenueCenter"""
    pvc0=[x[0] for x in res['popularVenueCenter']]
    aypvc=np.array([np.array(xi) for xi in pvc0])
    pvc1=[x[1] for x in res['popularVenueCenter']]
    axpvc=np.array([np.array(xi) for xi in pvc1])




    """distinct crimes and distinct roads"""
    mycurs.execute("""SELECT "targettype","PercentBurglaryUniq", num_agents, r.run_id
    FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and "targettype" is not null AND (start_date between '2017-11-02 13:51:20' and '2017-12-01') AND "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    res=collections.defaultdict(list)

    #each row is a run_id
    for row in results:
        print('UNIFORM')
        targettype=row[0]
        print(targettype)
        percent=float(row[1])
        agents=row[2]
        print(agents)
        runid=row[3]
        totaldist=float(40986771)

        mycurs.execute("""select sum(shape_leng) from (
        select distinct(run.road_id), road.shape_leng from open.res_la_roads run
        LEFT JOIN open.nyc_road_proj_final as road on road.gid=run.road_id WHERE run_id={}) as x
        """.format(runid))
        uDistance=mycurs.fetchall()
        uDist=float(uDistance[0][0])

        uniquePai=(percent)/(uDist/40986771)
        print(uniquePai)
        x=[uniquePai, agents]
        res[targettype].append(x)
        #print(res)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    byrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    bxrr=np.array([np.array(xi) for xi in rr1])

    #"""randomRoadCenter"""
    #rrc0=[x[0] for x in res['randomRoadCenter']]
    #yrrc=np.array([np.array(xi) for xi in rrc0])
    #rrc1=[x[1] for x in res['randomRoadCenter']]
    #xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    byrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    bxrv=np.array([np.array(xi) for xi in rv1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    byrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    bxrvc=np.array([np.array(xi) for xi in rvc1])

    """popularVenue"""
    pv0=[x[0] for x in res['popularVenue']]
    bypv=np.array([np.array(xi) for xi in pv0])
    pv1=[x[1] for x in res['popularVenue']]
    bxpv=np.array([np.array(xi) for xi in pv1])

    """popularVenueCenter"""
    pvc0=[x[0] for x in res['popularVenueCenter']]
    bypvc=np.array([np.array(xi) for xi in pvc0])
    pvc1=[x[1] for x in res['popularVenueCenter']]
    bxpvc=np.array([np.array(xi) for xi in pvc1])


    
    """distinct crimes and distinct roads"""
    mycurs.execute("""SELECT "targettype","PercentBurglaryUniq", num_agents, r.run_id
    FROM open.res_la_model AS m
    LEFT JOIN open.res_la_run r on m.run_id=r.run_id
    WHERE end_date is not null and step=29 and "targettype" is not null AND (start_date between '2017-11-02 13:51:20' and '2017-12-01') AND "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results[0])

    res=collections.defaultdict(list)

    #each row is a run_id
    for row in results:
        print('POWER')
        targettype=row[0]
        print(targettype)
        percent=float(row[1])
        agents=row[2]
        print(agents)
        runid=row[3]
        totaldist=float(40986771)

        mycurs.execute("""select sum(shape_leng) from (
        select distinct(run.road_id), road.shape_leng from open.res_la_roads run
        LEFT JOIN open.nyc_road_proj_final as road on road.gid=run.road_id WHERE run_id={}) as x
        """.format(runid))
        uDistance=mycurs.fetchall()
        uDist=float(uDistance[0][0])

        uniquePai=(percent)/(uDist/40986771)
        print(uniquePai)
        x=[uniquePai, agents]
        res[targettype].append(x)
        #print(res)

    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    cyrr=np.array([np.array(xi) for xi in rr0])
    rr1=[x[1] for x in res['randomRoad']]
    cxrr=np.array([np.array(xi) for xi in rr1])

    #"""randomRoadCenter"""
    #rrc0=[x[0] for x in res['randomRoadCenter']]
    #yrrc=np.array([np.array(xi) for xi in rrc0])
    #rrc1=[x[1] for x in res['randomRoadCenter']]
    #xrrc=np.array([np.array(xi) for xi in rrc1])

    """randomVenue"""
    rv0=[x[0] for x in res['randomVenue']]
    cyrv=np.array([np.array(xi) for xi in rv0])
    rv1=[x[1] for x in res['randomVenue']]
    cxrv=np.array([np.array(xi) for xi in rv1])

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    cyrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    cxrvc=np.array([np.array(xi) for xi in rvc1])

    """popularVenue"""
    pv0=[x[0] for x in res['popularVenue']]
    cypv=np.array([np.array(xi) for xi in pv0])
    pv1=[x[1] for x in res['popularVenue']]
    cxpv=np.array([np.array(xi) for xi in pv1])

    """popularVenueCenter"""
    cvc0=[x[0] for x in res['popularVenueCenter']]
    cypvc=np.array([np.array(xi) for xi in pvc0])
    cvc1=[x[1] for x in res['popularVenueCenter']]
    cxpvc=np.array([np.array(xi) for xi in pvc1])

    fig=plt.figure(1)
    ax=plt.subplot(111)

    plot1=plt.plot(axrr, ayrr, label='RandomRoad-U')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    plot3=plt.plot(axrv, ayrv, label='randomVenue-U')
    plot4=plt.plot(axrvc, ayrvc, label='randomVenueCenter-U')
    plot5=plt.plot(axpv, aypv, label='popularVenue-U')
    plot6=plt.plot(axpvc, aypvc, label='popularVenueCenter-U')

    plot1b=plt.plot(bxrr, byrr, label='RandomRoad-S')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    plot3b=plt.plot(bxrv, byrv, label='randomVenue-S')
    plot4b=plt.plot(bxrvc, byrvc, label='randomVenueCenter-S')
    plot5b=plt.plot(bxpv, bypv, label='popularVenue-S')
    plot6b=plt.plot(bxpvc, bypvc, label='popularVenueCenter-S')
    plt.axis([25,160,0,1])

    plot1c=plt.plot(cxrr, cyrr, label='RandomRoad-P')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    plot3c=plt.plot(cxrv, cyrv, label='randomVenue-P') 
    plot4c=plt.plot(cxrvc, cyrvc, label='randomVenueCenter-P')
    plot5c=plt.plot(cxpv, cypv, label='popularVenue-U')
    plot6c=plt.plot(cxpvc, cypvc, label='popularVenueCenter-P')

    ax.set_title('Unique adapted PAI for all crime types over n of agents')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique crimes adapted PAI')
    plt.legend()
    plt.show()






#hitCrimes()
#hitBurglary()
#hitRobbery()
#hitLarceny()
#hitLarcenyM()
#hitAssault()

#uniquePaiCrimes()

#uniquePaiCrimesS()
uniquePaiCrimesU()
#uniquePaiCrimesP()

#uniquePaiBurglary()