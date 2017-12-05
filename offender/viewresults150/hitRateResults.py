
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


#hitCrimes()
#hitBurglary()
#hitRobbery()
#hitLarceny()
#hitLarcenyM()
#hitAssault()