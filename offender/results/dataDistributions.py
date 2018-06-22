import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections


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

roadDist()
crimesPerRoad()
venuesPerRoad()