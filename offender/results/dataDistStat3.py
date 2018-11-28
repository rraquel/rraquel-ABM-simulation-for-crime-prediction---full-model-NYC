import numpy as np
import statistics
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections
import scipy.stats as sc
#from statsmodels.stats.contingency_tables import mcnemar


conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
mycurs = conn.cursor()

def stat():
    mycurs.execute("""select gid, occurrence_month, count(objectid) from open.nyc_police_incident2ct
        where exists (select gid from open.nyc_1percentcrimect where gid=open.nyc_police_incident2ct.gid) and not occurrence_month is null
        group by gid, occurrence_month order by gid""")
    items=mycurs.fetchall()

    gid=dict()

    for line in items:
        if line[0] in gid.keys():
            l=gid[line[0]]
            l.append((line[1], line[2]))
            gid[line[0]]=l
        else:
            gid[line[0]]=[(line[1], line[2])]

    print(len(gid.keys()))
    for key in gid.keys():
        month=dict()
        l=gid[key]
        for item in l:
            month[item[0]]=item[1]
        gid[key]=month
        mm=['Nov', 'Jun', 'Apr', 'Jan', 'Sep', 'Mar', 'Feb', 'May', 'Oct', 'Aug', 'Dec', 'Jul', ]
        for m in mm:
            if not m in month.keys():
                month[m]=0
                print('is 0')

    for key in gid.keys():
        month=gid[key]
        #print(month)
        i=list()
        for m in mm:
            i.append(month[m])
        ax=np.array(i)
        mean=statistics.mean(ax)
        sd=statistics.stdev(ax)

        print('gid: {0}, mean: {1}, sd: {2}'.format(key, mean, sd))




#createT()
#fillT()
stat()   
