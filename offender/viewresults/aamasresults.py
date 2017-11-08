import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections


conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
mycurs = conn.cursor()


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


    mycurs.execute("""SELECT r."targettype",PercentuniqueCrimes, m.num_agents, m.run_id
        FROM open.nyc_res_la_computenumagents5 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='uniformR'""")
    results5=mycurs.fetchall() #returns tuple with first row (unordered list)

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

    results=results100+results75+results50+results25+results5

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
    plt.axis([5,160,0,1])
    ax.set_title('adapted PAI(all crime) performance, Uniform distributed search radius')
    ax.set_xlabel('n of agents in simulation')
    ax.set_ylabel('unique adapted PAI')
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
        FROM open.nyc_res_la_computenumagents5 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='staticR'""")
    results5=mycurs.fetchall() #returns tuple with first row (unordered list)

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

    results=results100+results75+results50+results25+results5

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
        FROM open.nyc_res_la_computenumagents5 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        WHERE end_date is not null and "radiustype"='powerR'""")
    results5=mycurs.fetchall() #returns tuple with first row (unordered list)

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

    results=results100+results75+results50+results25+results5

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







#uniquePaiCrimes()

#uniquePaiCrimesS()
uniquePaiCrimesU()
#uniquePaiCrimesP()

#uniquePaiBurglary()