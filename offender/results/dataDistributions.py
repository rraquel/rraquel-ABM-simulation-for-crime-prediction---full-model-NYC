import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections
import scipy.stats as sc
#from statsmodels.stats.contingency_tables import mcnemar


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
    
def venueCatCorr():
    #categories=["'Arts & Entertainment'", "'College & University'", "'Event'", "'Food'", "'Nightlife Spot'", "'Outdoors & Recreation'", "'Professional & Other Places'", "'Residence'", "'Shop & Service'", "'Travel & Transport'"]
    #crimes=["'ROBBERY'", "'GRAND LARCENY'", "'FELONY ASSAULT'", "'BURGLARY'", "'GRAND LARCENY OF MOTOR VEHICLE'"]
    categories=["'Arts & Entertainment'", "'Travel & Transport'"]
    crimes=["'ROBBERY'", "'GRAND LARCENY OF MOTOR VEHICLE'"]
    #dictionary of categories with list assigned
    d=dict()
    #dictionary of roads
    r=dict()
    roads=list()
    crimescount=list()
    venuescount=list()
    #venues
    mycurs.execute("""SELECT distinct(r2.road_id) from open.nyc_road_proj_final  r
    left join open.nyc_road2fs_near2 r2 on r2.road_id=r.gid
    left join open.nyc_road2pi_5ft r3 on r3.road_id=r2.road_id""")
    res=mycurs.fetchall() #returns tuple with first row (unordered list)
    for row in res:
        road=row[0]
        roads.append(road)
        r[road]=0
    for cat in categories:
        mycurs.execute("""SELECT distinct(r2.road_id), count(distinct(venue_id))
        FROM open.nyc_fs_venue_join r
            left join open.nyc_road2fs_near2 r2 on r2.fs_id=r.venue_id
            where parent_name={} group by r2.road_id;""".format(cat))
        results=mycurs.fetchall() #returns tuple with first row (unordered list)
        venuescount=list()
        for row in results:
            r2=dict(r)
            venuec=row[1]
            road=row[0]
            r2[road]=venuec
        for road in roads:
            venuescount.append(r2[road])
        d[cat]=venuescount
    print(len(d[cat]))
    #crimes
    for cr in crimes:
        mycurs.execute("""SELECT distinct(road_id), count(distinct(object_id))
        FROM open.nyc_road_proj_final r
            left join open.nyc_road2pi_5ft r2 on r2.road_id=r.gid
            where offense={}  group by road_id""".format(cr))
        results=mycurs.fetchall() #returns tuple with first row (unordered list)
        print(results[0])
        crimescount=list()
        for row in results:
            r2=dict(r)
            crimec=row[1]
            road=row[0]
            print(crimec)
            r2[road]=crimec
        for road in roads:
            c=r2[road]
            print(c)
            crimescount.append(c)
        d[cr]=crimescount
    print(len(d[cr]))
    listx=list()
    lista=list()
    for cat in categories:
        a=list(d[cat])
        x=np.array(a)
        listx.append(x)
        lista.append(cat)
    for  cr in crimes:
        a=list(d[cat])
        x=np.array(a)
        listx.append(x)
        lista.append(cr)


    count=0
    count1=0
    for item in listx:
        count+=1
        count1=0
        for item2 in listx:
            count1+=1
            #erase same level 0:
            if not item.size==item2.size:
                print((item.size))
                print(item2.size)
                print("exit")
                exit()
            i=0
            while i<item.size-1:
                if item[i]==0 and item2[i]==0:
                    np.delete(item, i)
                    np.delete(item2, i)
            
            result=sc.pearsonr(item, item2)
            print("Pearson r{0}, {1}, correlation {2}".format(lista[count-1], lista[count1-1], result))
            result=sc.spearmanr(item, item2)
            print("Spearman r{0}, {1}, correlation {2}".format(lista[count-1], lista[count1-1], result))
    
    """
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

    """
    plt.hist(x, bins=50)
    plt.show()
        
    


#crimesPerCT()
#crimeCorr()
venueCatCorr()
#roadDist()
#crimesPerRoad()
#venuesPerRoad()