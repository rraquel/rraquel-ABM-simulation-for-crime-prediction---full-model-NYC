import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import collections



conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
mycurs = conn.cursor()



"""plot num agents vs hit rate (uniqueCrimes/total)"""
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

print(res['randomRoad'])

"""randomRoad"""
rr0=[x[0] for x in res['randomRoad']]
yrr=np.array([np.array(xi) for xi in rr0])
rr1=[x[1] for x in res['randomRoad']]
xrr=np.array([np.array(xi) for xi in rr1])
print(type(xrr))

"""randomRoadCenter"""
rrc0=[x[0] for x in res['randomRoadCenter']]
yrrc=np.array([np.array(xi) for xi in rrc0])
rrc1=[x[1] for x in res['randomRoadCenter']]
xrrc=np.array([np.array(xi) for xi in rrc1])
print(type(xrr))

"""randomVenueCenter"""
rvc0=[x[0] for x in res['randomVenueCenter']]
yrvc=np.array([np.array(xi) for xi in rvc0])
rvc1=[x[1] for x in res['randomVenueCenter']]
xrvc=np.array([np.array(xi) for xi in rvc1])
print(type(xrr))

"""randomVenue"""
rv0=[x[0] for x in res['randomVenue']]
yrv=np.array([np.array(xi) for xi in rv0])
rv1=[x[1] for x in res['randomVenue']]
xrv=np.array([np.array(xi) for xi in rv1])
print(type(xrr))

"""popularVenue"""
pv0=[x[0] for x in res['popularVenue']]
ypv=np.array([np.array(xi) for xi in pv0])
pv1=[x[1] for x in res['popularVenue']]
xpv=np.array([np.array(xi) for xi in pv1])
print(type(xrr))

"""popularVenueCenter"""
pvc0=[x[0] for x in res['popularVenueCenter']]
ypvc=np.array([np.array(xi) for xi in pvc0])
pvc1=[x[1] for x in res['popularVenueCenter']]
xpvc=np.array([np.array(xi) for xi in pvc1])
print(type(xrr))

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

"""plot unique crime hit rate vs. num of agent per strategy"""
#all cirmes
#select "uniqPai" from open.res_la_model where run_id=82 and step=1
#burlgary

#robbery

#larceny

#larcenyM

#assault