import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections


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

    """randomVenueType"""
    rvc0=[x[0] for x in res['randomVenueType']]
    yrvt=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueType']]
    xrvt=np.array([np.array(xi) for xi in rvc1])

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

    """popularVenueType"""
    pvc0=[x[0] for x in res['popularVenueType']]
    ypvt=np.array([np.array(xi) for xi in pvc0])
    pvc1=[x[1] for x in res['popularVenueType']]
    xpvt=np.array([np.array(xi) for xi in pvc1])


    fig=plt.figure(1)
    ax=plt.subplot(111)
    plot1=plt.plot(xrr, yrr, label='RandomRoad')
    plotall.append((xrr, yrr, 'RandomRoad'+dt))
    plotRR.append((xrr, yrr, 'RandomRoad'+dt))
    plotPVRR.append((xrr, yrr, 'RandomRoad'+dt))
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    #plotall.append(plot2)
    plot3=plt.plot(xrv, yrv, label='randomVenue')
    plotall.append((xrv, yrv, 'randomVenue'+dt))
    plot4=plt.plot(xrvc, yrvc, label='randomVenueCenter')
    plotall.append((xrvc, yrvc, 'randomVenueCenter'+dt))
    plot5=plt.plot(xrvt, yrvt, label='randomVenueType')
    plotall.append((xrvt, yrvt, 'randomVenueType'+dt))
    plot6=plt.plot(xpv, ypv, label='popularVenue')
    plotall.append((xpv, ypv, 'popularVenue'+dt))
    plotPV.append((xpv, ypv, 'popularVenue'+dt))
    plotPVRR.append((xpv, ypv, 'popularVenue'+dt))
    plot7=plt.plot(xpvc, ypvc, label='popularVenueCenter')
    plotall.append((xpvc, ypvc, 'popularVenueCenter'+dt))
    plotPV.append((xpvc, ypvc, 'popularVenueCenter'+dt))
    plot8=plt.plot(xpvt, ypvt, label='popularVenueType')
    plotall.append((xpvt, ypvt, 'popularVenueType'+dt))
    plotPV.append((xpvt, ypvt, 'popularVenueType'+dt))
    if type==0:
        plt.axis([25,1000,1.1,1.8])
        #plt.xticks([25, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000])
        plt.xticks([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
        #ax.set_title('adapted PAI - uniform distance')
        ax.set_xlabel('n of agents in scenario')
        ax.set_ylabel('unique adapted PAI')
    elif type==1:
        plt.axis([25,1000,50,100])
        #plt.xticks([25, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000])
        plt.xticks([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
        #plt.xticks([25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000])
        ax.set_title('Percent covered unique crimes')
        ax.set_xlabel('n of agents in scenario')
        ax.set_ylabel('% covered unique crimes')
    plt.legend()
    plt.show()

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

##################################################################################################################################################################    
"""===========plot ALL LINES target type and radius type per UNIQUE PAI========="""

def allPai():
    print("all PAI")
    #one color per distance search type
    #color=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    color=['b', 'g', 'c', 'y', 'k']
    
    fig=plt.figure(1)
    ax=plt.subplot(111)
    i=0
    x=0
    for p in plotall:
        c=color[x]
        plot=plt.plot(p[0], p[1], c, label=distancetype[x])
        if (i+1)%7==0:
            x+=1
        i+=1
    plt.axis([25,1000,1.1,1.8])
    #ax.set_title('adapted PAI - uniform distance')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()

def RRPai():
    print("random road")
    #one color per distance search type
    #color=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    fig=plt.figure(1)
    ax=plt.subplot(111)
    i=0
    x=0
    for p in plotRR:
        #c=color[x]
        #plot=plt.plot(p[0], p[1], c, label=p[2])
        plot=plt.plot(p[0], p[1], label=p[2])
        if (i+1)%7==0:
            x+=1
        i+=1
    plt.axis([25,1000,1.1,1.8])
    #ax.set_title('adapted PAI - uniform distance')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()

def PVPai():
    print("popular venue")
    #one color per distance search type
    #color=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    fig=plt.figure(1)
    ax=plt.subplot(111)
    i=0
    x=0
    for p in plotPV:
        #c=color[x]
        #plot=plt.plot(p[0], p[1], c, label=p[2])
        plot=plt.plot(p[0], p[1], label=p[2])
        if (i+1)%7==0:
            x+=1
        i+=1
    plt.axis([25,1000,1.1,1.8])
    #ax.set_title('adapted PAI - uniform distance')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()

def RRPVPai():
    #one color per distance search type
    print("Random road and popular venue")
    color=['b', 'g']
    fig=plt.figure(1)
    ax=plt.subplot(111)
    i=0
    x=0
    for p in plotPVRR:
        #c=color[x]
        if i % 2 == 0:
            c=color[0]
        else:
            c=color[1]
        plot=plt.plot(p[0], p[1], c, label=p[2])
        i+=1
    plt.axis([25,1000,1.1,1.8])
    #ax.set_title('adapted PAI - uniform distance')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()

    
def avgPai():
    mycurs.execute("""SELECT a.run_id, average, distancetype, targettype FROM (
        SELECT run_id, AVG(uniqpai) as average
        FROM abm_res.res_la_results1000agent group by run_id) as a
        left join abm_res.res_la_runprototype b on a.run_id=b.run_id""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)
    #print(results)
    paiavg=list()
    for row in results:
        r=row[0]
        paiavg.append(float(row[1]))
    x=np.array(paiavg)
    fig=plt.figure(1)
    plot1=plt.hist(x, bins=50)
    #plt.xlim(0,60)
    #plt.title('venue count for each road distribution')
    plt.xlabel('number of venues per road')
    plt.ylabel('frequency')
    plt.legend()
    plt.show()



################################################################################################################################################################## 

"""===========plot target type and radius type per UNIQUE PAI========="""

def uniquePercentCrimes():
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""
    for dt in distancetype:
        mycurs.execute("""SELECT "targettype", PercentuniqueCrimes, num_agents, run_id
        FROM abm_res.res_la_results1000agent
        WHERE "distancetype"='{0}'""".format(dt))
        results=mycurs.fetchall() #returns tuple with first row (unordered list)
        print('Percent {}'.format(dt))
        buildCases(results, 1, dt)

##################################################################################################################################################################    

"""===========plot BEST target type and radius type per UNIQUE PAI========="""

def uniquePaiCrimesBest():
    """----------ALL CRIMES----------"""
    """combines best target type strategies per radius search"""
    mycurs.execute("""SELECT "targettype", uniqPai, num_agents, run_id
    FROM abm_res.res_la_results1000agent
    Where '{0}'""".format(run_ids))
    resultstotal=mycurs.fetchall() #returns tuple with first row (unordered list)
    
    res=collections.defaultdict(list)
    #print('best combineds')
    #each row is a run_id
    for row in resultstotal:
        targettype=row[0]
        #print(targettype)
        uniquePai=float(row[1])
        agents=row[2]
        #print(agents)
        runid=row[3]
        x=[uniquePai, agents]
        res[targettype].append(x)
        #print(res)

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
    #plt.axis([5,160,1,2])
    plt.axis([25,1000,0,3])
    #ax.set_title('adapted PAI - comparing best performing scenarios')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()

################################################################################################################################################################## 

"""===========plot frequency of roads traveled for BEST strategy and wors strategy========="""

def roadFrequency():
    for r in run_ids2:
        mycurs.execute("""SELECT road_id, count(road_id) as c
           FROM abm_res.res_la_roadsprototype
           WHERE run_id='{0}' 
           GROUP BY road_id
           UNION
           SELECT gid, 0
           FROM open.nyc_road_proj_final
           WHERE gid NOT IN (SELECT road_id FROM abm_res.res_la_roadsprototype WHERE run_id='{1}')""".format(r, r))

        results=mycurs.fetchall() #returns tuple with first row (unordered list)

        #each row is a run_id
        roadcount=list()
        for row in results:
            roadid=row[0]
            roadcount.append(float(row[1]))

        x=np.array(roadcount)
        print(max(x))
        fig=plt.figure(1)
        plot1=plt.hist(x, bins=50)
        #plt.xlim(0,60)
        #plt.title('venue count for each road distribution')
        plt.xlabel('number of venues per road')
        plt.ylabel('frequency')
        plt.legend()
        plt.show()

################################################################################################################################################################## 

plotall=list()
plotRR=list()
plotPV=list()
plotPVRR=list()
#distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract', 'taxiTractD', 'crimeTractM', 'crimeTractMD', 'crimeTract1x12', 'crimeTract1x12D', 'crimeTract1x6', 'crimeTract1']
distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract', 'crimeTractMD']
#distancetype=['staticR', 'uniformR', 'powerR', 'taxiTract']
"""PAI"""
uniquePaiCrimes()
#plot all:
#allPai()
#RRPai()
#RR with crime tract performs best
#PVPai()
#RRPVPai()
#avgPai()
"""
StaticR -popular venue center
unform - popular venue center
power -
taxitract -popular venue
crimeMD -popular venue center
"""

"""Percent"""
#uniquePercentCrimes()


#unique results best combined
run_ids=['run_id=620 OR run_id=621']
#uniquePaiCrimesBest()
#frequency roads traveled best and wors strategy
run_ids2=[620, 621]
#roadFrequency()