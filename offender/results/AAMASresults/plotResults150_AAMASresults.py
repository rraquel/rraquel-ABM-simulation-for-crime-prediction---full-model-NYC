import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections


conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
mycurs = conn.cursor()


"""===========plot target type and radius type per UNIQUE PAI========="""


def uniquePaiCrimesS():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""

    mycurs.execute("""SELECT "targettype", uniqPai, num_agents, run_id
        FROM open.res_la_results150agent AS m
        WHERE  "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)

    res=collections.defaultdict(list)
    print('STATIC')
    #each row is a run_id
    for row in results:
        targettype=row[0]
        print(targettype)
        uniquePai=float(row[1])
        print(uniquePai)
        agents=row[2]
        print(agents)
        runid=row[3]
        x=[uniquePai, agents]
        res[targettype].append(x)
        #print(res)




    """randomRoad"""
    rr0=[x[0] for x in res['randomRoad']]
    #print(rr0)
    yrr=np.array([np.array(xi) for xi in rr0])
    #print(yrr)
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
    print(rv1)
    xrv=np.array([np.array(xi) for xi in rv1])
    print(xrv)

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
    plt.axis([25,150,1,2])
    plt.xticks([25,50,75,100,125,150])
    #ax.set_title('adapted PAI - static distance')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique crimes adapted PAI')
    plt.legend()
    plt.show()




def uniquePaiCrimesU():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""

    mycurs.execute("""SELECT "targettype",uniqPai, num_agents, run_id
        FROM open.res_la_results150agent AS m
        WHERE "radiustype"='uniformR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)

    res=collections.defaultdict(list)
    print('UNIFORM')
    #each row is a run_id
    for row in results:
        targettype=row[0]
        print(targettype)
        uniquePai=float(row[1])
        print(uniquePai)
        agents=row[2]
        print(agents)
        runid=row[3]
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
    plt.axis([25,150,1,2])
    plt.xticks([25,50,75,100,125,150])
    #ax.set_title('adapted PAI - uniform distance')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()


def uniquePaiCrimesP():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""

    mycurs.execute("""SELECT "targettype", uniqPai, num_agents, run_id
        FROM open.res_la_results150agent
        WHERE  "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)

    res=collections.defaultdict(list)
    print('POWER')
    #each row is a run_id
    for row in results:
        targettype=row[0]
        print(targettype)
        uniquePai=float(row[1])
        agents=row[2]
        print(agents)
        runid=row[3]
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
    plt.axis([25,150,1,2])
    plt.xticks([25,50,75,100,125,150])
    #ax.set_title('adapted PAI - Lévy distance')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique crimes adapted PAI')
    plt.legend()
    plt.show()


##################################################################################################################################################################    

def uniquePaiCrimesBest():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """combines best target type strategies per radius search"""

    mycurs.execute("""SELECT "targettype", uniqPai, num_agents, run_id
        FROM open.res_la_results150agent
        Where run_id=2 or run_id=285 or run_id=5""")
    resultstotal=mycurs.fetchall() #returns tuple with first row (unordered list)
    
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
    plot4=plt.plot(xrvc, yrvc, label='static distance - randomVenueCenter destination')
    plot6=plt.plot(xpvc, ypvc, label='uniform distance - popularVenueCenter destination')
    plot5=plt.plot(xpv, ypv, label='Lévy flight distance - popularVenue destination')
    #plt.axis([5,160,1,2])
    plt.axis([25,150,1,2])
    plt.xticks([25,50,75,100,125,150])
    #ax.set_title('adapted PAI - comparing best performing scenarios')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()

################################################################################################################################################################## 

"""===========plot target type and radius type per UNIQUE PAI========="""

def uniquePercentCrimesU():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""

    mycurs.execute("""SELECT "targettype", PercentuniqueCrimes, num_agents, run_id
        FROM open.res_la_results150agent
        WHERE "radiustype"='uniformR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)


    res=collections.defaultdict(list)
    print('UNIFORM')
    #each row is a run_id
    for row in results:
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
    plot1=plt.plot(xrr, yrr, label='RandomRoad')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    plot3=plt.plot(xrv, yrv, label='randomVenue')
    plot4=plt.plot(xrvc, yrvc, label='randomVenueCenter')
    plot5=plt.plot(xpv, ypv, label='popularVenue')
    plot6=plt.plot(xpvc, ypvc, label='popularVenueCenter')
    plt.axis([25,150,0,100])
    plt.xticks([25,50,75,100,125,150])
    ax.set_title('Percent covered unique crimes - uniform distance')
    ax.set_xlabel('n of agents in simulation')
    ax.set_ylabel('% covered unique crimes')
    plt.legend()
    plt.show()


def uniquePercentCrimesS():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""

    mycurs.execute("""SELECT "targettype", PercentuniqueCrimes, num_agents, run_id
        FROM open.res_la_results150agent
        WHERE  "radiustype"='staticR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)


    res=collections.defaultdict(list)
    print('STATIC')
    #each row is a run_id
    for row in results:
        targettype=row[0]
        print(targettype)
        uniquePercent=float(row[1])*100
        print(uniquePercent)
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
    plot1=plt.plot(xrr, yrr, label='RandomRoad')
    #plot2=plt.plot(xrrc, yrrc, label='RandomRoadCenter')
    plot3=plt.plot(xrv, yrv, label='randomVenue')
    plot4=plt.plot(xrvc, yrvc, label='randomVenueCenter')
    plot5=plt.plot(xpv, ypv, label='popularVenue')
    plot6=plt.plot(xpvc, ypvc, label='popularVenueCenter')
    plt.axis([25,150,0,100])
    plt.xticks([25,50,75,100,125,150])
    ax.set_title('Percent covered unique crimes - static distance')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('% covered unique crimes')
    plt.legend()
    plt.show()


def uniquePercentCrimesP():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""

    mycurs.execute("""SELECT "targettype", PercentuniqueCrimes, num_agents, run_id
        FROM open.res_la_results150agent
        WHERE  "radiustype"='powerR'""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)


    res=collections.defaultdict(list)
    print('POWER')
    #each row is a run_id
    for row in results:
        targettype=row[0]
        print(targettype)
        uniquePercent=float(row[1])*100
        agents=row[2]
        print(agents)
        runid=row[3]
        x=[uniquePercent, agents]
        res[targettype].append(x)
        print(res)


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
    plt.axis([25,150,0,100])
    plt.xticks([25,50,75,100,125,150])
    ax.set_title('Percent covered unique crimes - Lévy distance')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('% covered unique crimes')
    plt.legend()
    plt.show()

#-------------------------------------------------Best PAI combined----------------------------------------------

def uniquePaiCrimesBest():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """combines best target type strategies per radius search"""

    mycurs.execute("""SELECT "targettype", uniqPai, num_agents, run_id
   FROM open.res_la_results150agent
   Where run_id=2 or run_id=285 or run_id=5""")
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
        #print(runid)
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
    print(pv0)
    ypv=np.array([np.array(xi) for xi in pv0])
    pv1=[x[1] for x in res['popularVenue']]
    print(pv1)
    xpv=np.array([np.array(xi) for xi in pv1])

    """popularVenueCenter"""
    pvc0=[x[0] for x in res['popularVenueCenter']]
    ypvc=np.array([np.array(xi) for xi in pvc0])
    pvc1=[x[1] for x in res['popularVenueCenter']]
    xpvc=np.array([np.array(xi) for xi in pvc1])

    fig=plt.figure(1)
    ax=plt.subplot(111)
    plot4=plt.plot(xrvc, yrvc, label='static distance - randomVenueCenter destination')
    plot6=plt.plot(xpvc, ypvc, label='uniform distance - popularVenueCenter destination')
    plot5=plt.plot(xpv, ypv, label='Lévy flight distance - popularVenue destination')
    #plt.axis([5,160,1,2])
    plt.axis([25,150,1,2])
    plt.xticks([25,50,75,100,125,150])
    #ax.set_title('adapted PAI - comparing best performing scenarios')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()





#-------------------------------------------------Best Percentage crime types----------------------------------------------

def uniquePercentCrimesBest():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""

    mycurs.execute("""SELECT "targettype", PercentuniqueCrimes, num_agents, run_id
   FROM open.res_la_results150agent
   Where run_id=2 or run_id=285 or run_id=5""")
    resultstotal=mycurs.fetchall() #returns tuple with first row (unordered list)
    
    res=collections.defaultdict(list)
    #print('best combineds')
    #each row is a run_id
    for row in resultstotal:
        targettype=row[0]
        #print(targettype)
        uniquePercent=float(row[1])*100
        agents=row[2]
        #print(agents)
        runid=row[3]
        #print(runid)
        x=[uniquePercent, agents]
        res[targettype].append(x)
        #print(res)

    """randomVenueCenter"""
    rvc0=[x[0] for x in res['randomVenueCenter']]
    yrvc=np.array([np.array(xi) for xi in rvc0])
    rvc1=[x[1] for x in res['randomVenueCenter']]
    xrvc=np.array([np.array(xi) for xi in rvc1])

    """popularVenue"""
    pv0=[x[0] for x in res['popularVenue']]
    print(pv0)
    ypv=np.array([np.array(xi) for xi in pv0])
    pv1=[x[1] for x in res['popularVenue']]
    print(pv1)
    xpv=np.array([np.array(xi) for xi in pv1])

    """popularVenueCenter"""
    pvc0=[x[0] for x in res['popularVenueCenter']]
    ypvc=np.array([np.array(xi) for xi in pvc0])
    pvc1=[x[1] for x in res['popularVenueCenter']]
    xpvc=np.array([np.array(xi) for xi in pvc1])

    fig=plt.figure(1)
    ax=plt.subplot(111)
    plot4=plt.plot(xrvc, yrvc, label='static distance - randomVenueCenter destination')
    plot6=plt.plot(xpvc, ypvc, label='uniform distance - popularVenueCenter destination')
    plot5=plt.plot(xpv, ypv, label='Lévy flight distance - popularVenue destination')
    #plt.axis([5,160,1,2])
    plt.axis([25,150,0,100])
    plt.xticks([25,50,75,100,125,150])
    #ax.set_title('adapted PAI - comparing best performing scenarios')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()



#------------------------------------------------Crime Types----------------------------------------------
def uniquePaiCrimesBestB():


    """----------ALL CRIMES----------"""
    """combines best target type strategies per radius search"""

    bestRun_ids='(run_id=2 or run_id=285 or run_id=5)'

    mycurs.execute("""SELECT "targettype",uniquePaiBurglary,
        uniquePaiRobbery, uniquePaiLarceny, uniquePaiLarcneyM,
        uniquePaiAssault, num_agents, run_id, uniqPai
        FROM open.res_la_results150agent
        where {}""".format(bestRun_ids))
    resultstotal = mycurs.fetchall()  # returns tuple with first row (unordered list)


    res2 = collections.defaultdict(list)
    res285 = collections.defaultdict(list)
    res5= collections.defaultdict(list)

    print('best combineds')
    #each row is a run_id
    for row in resultstotal:
        runid = row[7]
        if runid==2:
            targettype = row[0]
            uniquePaiB = float(row[1])
            uniquePaiR = float(row[2])
            uniquePaiL = float(row[3])
            uniquePaiLM = float(row[4])
            uniquePaiA = float(row[5])
            print(uniquePaiA)
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
            print(a)
            c = [uniqPai, agents]
            crimetype = 'c'
            res2[crimetype].append(c)

        


    rr0 = [x[0] for x in res2['b']]
    yrr = np.array([np.array(xi) for xi in rr0])
    rr1 = [x[1] for x in res2['b']]
    xrr = np.array([np.array(xi) for xi in rr1])

    rrc0 = [x[0] for x in res2['r']]
    yrrc = np.array([np.array(xi) for xi in rrc0])
    rrc1 = [x[1] for x in res2['r']]
    xrrc = np.array([np.array(xi) for xi in rrc1])

    rv0 = [x[0] for x in res2['l']]
    yrv = np.array([np.array(xi) for xi in rv0])
    rv1 = [x[1] for x in res2['l']]
    xrv = np.array([np.array(xi) for xi in rv1])

    rvc0 = [x[0] for x in res2['m']]
    yrvc = np.array([np.array(xi) for xi in rvc0])
    rvc1 = [x[1] for x in res2['m']]
    xrvc = np.array([np.array(xi) for xi in rvc1])

    pv0 = [x[0] for x in res2['a']]
    ypv = np.array([np.array(xi) for xi in pv0])
    pv1 = [x[1] for x in res2['a']]
    xpv = np.array([np.array(xi) for xi in pv1])

    pv2 = [x[0] for x in res2['c']]
    ypv2 = np.array([np.array(xi) for xi in pv2])
    pv2 = [x[1] for x in res2['c']]
    xpv2 = np.array([np.array(xi) for xi in pv2])

    fig = plt.figure(1)
    ax = plt.subplot(111)
    plot1 = plt.plot(xrr, yrr, label='Burglary')
    plot2 = plt.plot(xrrc, yrrc, label='Robbery')
    plot3 = plt.plot(xrv, yrv, label='Grand Larceny')
    plot4 = plt.plot(xrvc, yrvc, label='Grand Larceny Motor Vehicle')
    plot5 = plt.plot(xpv, ypv, label='Felony Assault')
    plot6 = plt.plot(xpv2, ypv2, label='All Crime types', color='k', linewidth=3)
    #plt.axis([5, 160, 1, 2.1])
    plt.axis([25,150,1,2])
    plt.xticks([25,50,75,100,125,150])
    #ax.set_title('adapted PAI - comparing best performing scenarios')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()


  


uniquePaiCrimesS()
uniquePaiCrimesU()
uniquePaiCrimesP()

#uniquePercentCrimesS()
#uniquePercentCrimesU()
#uniquePercentCrimesP()

#unique results best combined
uniquePaiCrimesBest()

#percentage Best
uniquePercentCrimesBest()

#crime types for best performing
uniquePaiCrimesBestB()