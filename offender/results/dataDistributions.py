import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections
import scipy.stats as sc
from statsmodels.stats.contingency_tables import mcnemar


conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
mycurs = conn.cursor()


"""===========plot target type and radius type per UNIQUE PAI========="""

def roadDist():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""

    mycurs.execute("""select r.gid,length from 
            open.nyc_intersection2road i2r
            left join open.nyc_road_proj_final r on i2r.road_id = r. gid
            left join open.nyc_road_attributes ra on ra.road_id=r.gid""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)

    #each row is a run_id
    length=list()
    for row in results:
        roadid=row[0]
        length.append(float(row[1]))

    x=np.array(length)
    print(max(x))
    fig=plt.figure(1)
    plot1=plt.hist(x, bins=50)
    #plt.xlim(0,2000)
    #plt.title('road lenght count distribution')
    plt.xlabel('road length in ft')
    plt.ylabel('frequency')
    plt.legend()
    plt.show()


def crimesPerRoad():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""

    mycurs.execute("""SELECT
    road_id, COUNT(object_id)
    FROM
    open.nyc_road2police_incident_5ft_types_Jun
    GROUP BY
    road_id
    HAVING 
    COUNT(*) > 1""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)

    #each row is a run_id
    crimecount=list()
    for row in results:
        roadid=row[0]
        crimecount.append(float(row[1]))

    x=np.array(crimecount)
    print(max(x))
    fig=plt.figure(1)
    plot1=plt.hist(x, bins=50)
    #plt.xlim(0,10)
    #plt.title('crimes count for each road distribution')
    plt.xlabel('number crimes per road')
    plt.ylabel('frequency')
    plt.legend()
    plt.show()


def venuesPerRoad():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""

    mycurs.execute("""SELECT road_id, COUNT(fs_id)
    FROM
    open.nyc_road2fs_near2
    GROUP BY
    road_id
    HAVING 
    COUNT(*) > 1""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)

    #each row is a run_id
    venuecount=list()
    for row in results:
        roadid=row[0]
        venuecount.append(float(row[1]))

    x=np.array(venuecount)
    print(max(x))
    fig=plt.figure(1)
    plot1=plt.hist(x, bins=50)
    #plt.xlim(0,60)
    #plt.title('venue count for each road distribution')
    plt.xlabel('number of venues per road')
    plt.ylabel('frequency')
    plt.legend()
    plt.show()


def crimesPerCT():

    ####
    ####TODO erase LIMIT 2
    """----------ALL CRIMES----------"""
    """distinct crimes and distinct roads"""

    mycurs.execute("""SELECT
    gid, COUNT(*)
    FROM
    open.nyc_police_incident2CT
    WHERE occurence_year=2015 and occurrence_month='Jan'
    GROUP BY
    gid
    HAVING 
    COUNT(*) > 1""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)

    #each row is a run_id
    crimecount=list()
    for row in results:
        roadid=row[0]
        crimecount.append(float(row[1]))

    x=np.array(crimecount)
    print(max(x))
    fig=plt.figure(1)
    plot1=plt.hist(x, bins=50)
    #plt.xlim(0,10)
    #plt.title('crimes count for each road distribution')
    plt.xlabel('number crimes per census tract')
    plt.ylabel('frequency')
    plt.legend()
    plt.show()

def crimeCorr():

    mycurs.execute("""select gid, may, june, jan, feb, mar, apr, jul, jun14 FROM open.nyc_police_incident2CT_month""")
    results=mycurs.fetchall() #returns tuple with first row (unordered list)

    #each row is a run_id
    crimecmay=list()
    crimecjun=list()
    crimecjan=list()
    crimecfeb=list()
    crimecmar=list()
    crimecapr=list()
    crimecjul=list()
    crimecjun14=list()

    for row in results:
        gid=row[0]
        may=row[1]
        jun=row[2]
        jan=row[3]
        feb=row[4]
        mar=row[5]
        apr=row[6]
        jul=row[7]
        jun14=row[8]
        crimecmay.append(may)
        crimecjun.append(jun)
        crimecjan.append(jan)
        crimecfeb.append(feb)
        crimecmar.append(mar)
        crimecapr.append(apr)
        crimecjul.append(jul)
        crimecjun14.append(jun14)

    x=np.array(crimecmay)
    z=np.array(crimecjun)
    y=np.array(crimecjan)
    w=np.array(crimecfeb)
    s=np.array(crimecmar)
    q=np.array(crimecapr)
    p=np.array(crimecjul)
    t=np.array(crimecjun14)

    listx=[x, z, y, w, s, q, p, t]

    count=0
    count1=0
    for item in listx:
        count+=1
        count1=0
        for item2 in listx:
            count1+=1
            result=sc.spearmanr(item, item2)
            print("{0}, {1}, correlation {2}".format(count, count1, result))
    

    a=sc.spearmanr(x, z)
    print("may and june {}".format(a))
    b=sc.spearmanr(y, z)
    print("may and jan {}".format(b))
    c=sc.spearmanr(y, w)
    print("jan and feb {}".format(c))
    d=sc.spearmanr(z, w)
    print("jun and feb {}".format(d))
    e=sc.spearmanr(s, w)
    print("mar and feb {}".format(e))
    f=sc.spearmanr(s, z)
    print("mar and jun {}".format(f))
    g=sc.spearmanr(q, w)
    print("mar and feb {}".format(g))
    h=sc.spearmanr(q, z)
    print("mar and jun {}".format(h))   
    k=sc.spearmanr(t, z)
    print("jun14 and jun15 {}".format(k))  

    xz=np.column_stack((x, z))
    tz=np.column_stack((t, z))

    a2=mcnemar(xz)
    print("may and june {}".format(a2.statistic))
    print("may and june {}".format(a2.pvalue))
    if a2.pvalue > 0.05:
    	print('Same proportions')
    else:
	    print('Different proportions')
    k2=mcnemar(tz)
    print("jun14 and jun15 {}".format(k2.statistic))
    print("jun14 and jun15 {}".format(k2.pvalue)) 
    if k2.pvalue > 0.05:
        	print('Same proportions')
    else:
	    print('Different proportions')


    plt.hist(x, bins=50)
    plt.show()
    
    
    


#crimesPerCT()
crimeCorr()
#roadDist()
#crimesPerRoad()
#venuesPerRoad()