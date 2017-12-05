import numpy as np
import psycopg2
import sys
import os
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections


conn = psycopg2.connect(
    "dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")
mycurs = conn.cursor()


"""===========plot target type and radius type per UNIQUE PAI========="""


def uniquePaiCrimesBestB():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """combines best target type strategies per radius search"""

    mycurs.execute("""SELECT r."targettype",uniquePaiBurglary,
        uniquePaiRobbery, uniquePaiLarceny, uniquePaiLarcneyM,
        uniquePaiAssault, m.num_agents, m.run_id, uniqPai
        FROM open.nyc_res_la_computenumagents5 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results = mycurs.fetchall()  # returns tuple with first row (unordered list)
    resultstotal = results

    mycurs.execute("""SELECT r."targettype",uniquePaiBurglary,
        uniquePaiRobbery, uniquePaiLarceny, uniquePaiLarcneyM,
        uniquePaiAssault, m.num_agents, m.run_id, uniqPai
        FROM open.nyc_res_la_computenumagents25 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results = mycurs.fetchall()  # returns tuple with first row (unordered list)
    resultstotal = resultstotal + results

    mycurs.execute("""SELECT r."targettype",uniquePaiBurglary,
        uniquePaiRobbery, uniquePaiLarceny, uniquePaiLarcneyM,
        uniquePaiAssault, m.num_agents, m.run_id, uniqPai
        FROM open.nyc_res_la_computenumagents50 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results = mycurs.fetchall()  # returns tuple with first row (unordered list)
    resultstotal = resultstotal + results

    mycurs.execute("""SELECT r."targettype",uniquePaiBurglary,
    uniquePaiRobbery, uniquePaiLarceny, uniquePaiLarcneyM,
    uniquePaiAssault, m.num_agents, m.run_id, uniqPai
        FROM open.nyc_res_la_computenumagents75 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results = mycurs.fetchall()  # returns tuple with first row (unordered list)
    resultstotal = resultstotal + results

    mycurs.execute("""SELECT r."targettype",uniquePaiBurglary,
    uniquePaiRobbery, uniquePaiLarceny, uniquePaiLarcneyM,
    uniquePaiAssault, m.num_agents, m.run_id, uniqPai
        FROM open.nyc_res_la_computenumagents100 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results = mycurs.fetchall()  # returns tuple with first row (unordered list)
    resultstotal = resultstotal + results

    mycurs.execute("""SELECT r."targettype",uniquePaiBurglary,
        uniquePaiRobbery, uniquePaiLarceny, uniquePaiLarcneyM,
        uniquePaiAssault, m.num_agents, m.run_id, uniqPai
        FROM open.nyc_res_la_computenumagents125 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results = mycurs.fetchall()  # returns tuple with first row (unordered list)
    resultstotal = resultstotal + results

    mycurs.execute("""SELECT r."targettype",uniquePaiBurglary,
    uniquePaiRobbery, uniquePaiLarceny, uniquePaiLarcneyM,
    uniquePaiAssault, m.num_agents, m.run_id, uniqPai
        FROM open.nyc_res_la_computenumagents150 AS m
        LEFT JOIN open.res_la_run r on m.run_id=r.run_id
        Where r.run_id=2 or r.run_id=285 or r.run_id=5""")
    results = mycurs.fetchall()  # returns tuple with first row (unordered list)
    resultstotal = resultstotal + results

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
    plt.axis([25, 160, 1, 2.1])
    #ax.set_title('adapted PAI - comparing best performing scenarios')
    ax.set_xlabel('n of agents in scenario')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()


  
uniquePaiCrimesBestB()


"""

elif runid == 285:
            targettype = row[0]
            print(targettype)
            uniquePaiB = float(row[1])
            uniquePaiR = float(row[2])
            uniquePaiL = float(row[3])
            uniquePaiLM = float(row[4])
            uniquePaiA = float(row[5])
            agents = row[6]
            print(agents)
            runid = row[7]
            b = [uniquePaiB, agents]
            crimetype = 'b'
            res285[crimetype].append(b)
            r = [uniquePaiR, agents]
            crimetype = 'r'
            res285[crimetype].append(r)
            l = [uniquePaiL, agents]
            crimetype = 'l'
            res285[crimetype].append(l)
            m = [uniquePaiLM, agents]
            crimetype = 'm'
            res285[crimetype].append(m)
            a = [uniquePaiA, agents]
            crimetype = 'a'
            res285[crimetype].append(a)

        elif runid ==5:
            targettype = row[0]
            uniquePaiB = float(row[1])
            uniquePaiR = float(row[2])
            uniquePaiL = float(row[3])
            uniquePaiLM = float(row[4])
            uniquePaiA = float(row[5])
            print(uniquePaiA)
            agents = row[6]
            runid = row[7]
            b = [uniquePaiB, agents]
            crimetype = 'b'
            res5[crimetype].append(b)
            r = [uniquePaiR, agents]
            crimetype = 'r'
            res5[crimetype].append(r)
            l = [uniquePaiL, agents]
            crimetype = 'l'
            res5[crimetype].append(l)
            m = [uniquePaiLM, agents]
            crimetype = 'm'
            res5[crimetype].append(m)
            a = [uniquePaiA, agents]
            crimetype = 'a'
            res5[crimetype].append(a)
            c = [uniqPai, agents]
            crimetype = 'c'
            res5[crimetype].append(c)




  rr0 = [x[0] for x in res285['b']]
    yrr = np.array([np.array(xi) for xi in rr0])
    rr1 = [x[1] for x in res285['b']]
    xrr = np.array([np.array(xi) for xi in rr1])

    rrc0 = [x[0] for x in res285['r']]
    yrrc = np.array([np.array(xi) for xi in rrc0])
    rrc1 = [x[1] for x in res285['r']]
    xrrc = np.array([np.array(xi) for xi in rrc1])

    rv0 = [x[0] for x in res285['l']]
    yrv = np.array([np.array(xi) for xi in rv0])
    rv1 = [x[1] for x in res285['l']]
    xrv = np.array([np.array(xi) for xi in rv1])

    rvc0 = [x[0] for x in res285['m']]
    yrvc = np.array([np.array(xi) for xi in rvc0])
    rvc1 = [x[1] for x in res285['m']]
    xrvc = np.array([np.array(xi) for xi in rvc1])

    pv0 = [x[0] for x in res285['a']]
    ypv = np.array([np.array(xi) for xi in pv0])
    pv1 = [x[1] for x in res285['a']]
    xpv = np.array([np.array(xi) for xi in pv1])

    fig = plt.figure(1)
    ax = plt.subplot(111)
    plot1 = plt.plot(xrr, yrr, label='Burglary')
    plot2 = plt.plot(xrrc, yrrc, label='Robbery')
    plot3 = plt.plot(xrv, yrv, label='Grand Larceny')
    plot4 = plt.plot(xrvc, yrvc, label='Grand Larceny Motor Vehicle')
    plot5 = plt.plot(xpv, ypv, label='Felony Assault')
    plt.axis([5, 160, 1,2.1])
    #ax.set_title('adapted PAI - comparing best performing scenarios')
    ax.set_xlabel('n of agents in simulation')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()



    rr0 = [x[0] for x in res5['b']]
    yrr = np.array([np.array(xi) for xi in rr0])
    rr1 = [x[1] for x in res5['b']]
    xrr = np.array([np.array(xi) for xi in rr1])

    rrc0 = [x[0] for x in res5['r']]
    yrrc = np.array([np.array(xi) for xi in rrc0])
    rrc1 = [x[1] for x in res5['r']]
    xrrc = np.array([np.array(xi) for xi in rrc1])

    rv0 = [x[0] for x in res5['l']]
    yrv = np.array([np.array(xi) for xi in rv0])
    rv1 = [x[1] for x in res5['l']]
    xrv = np.array([np.array(xi) for xi in rv1])

    rvc0 = [x[0] for x in res5['m']]
    yrvc = np.array([np.array(xi) for xi in rvc0])
    rvc1 = [x[1] for x in res5['m']]
    xrvc = np.array([np.array(xi) for xi in rvc1])

    pv0 = [x[0] for x in res5['a']]
    ypv = np.array([np.array(xi) for xi in pv0])
    pv1 = [x[1] for x in res5['a']]
    xpv = np.array([np.array(xi) for xi in pv1])

    fig = plt.figure(1)
    ax = plt.subplot(111)
    plot1 = plt.plot(xrr, yrr, label='Burglary')
    plot2 = plt.plot(xrrc, yrrc, label='Robbery')
    plot3 = plt.plot(xrv, yrv, label='Grand Larceny')
    plot4 = plt.plot(xrvc, yrvc, label='Grand Larceny Motor Vehicle')
    plot5 = plt.plot(xpv, ypv, label='Felony Assault')
    plt.axis([5, 160, 1, 2.1])
    #ax.set_title('adapted PAI - comparing best performing scenarios')
    ax.set_xlabel('n of agents in simulation')
    ax.set_ylabel('unique adapted PAI')
    plt.legend()
    plt.show()
    """
