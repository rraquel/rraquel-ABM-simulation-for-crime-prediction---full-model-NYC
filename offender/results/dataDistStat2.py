import numpy as np
import psycopg2, sys, os, time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import collections
import scipy.stats as sc
#from statsmodels.stats.contingency_tables import mcnemar


conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
mycurs = conn.cursor()

  
def createT():
    for cat in categories2:
        mycurs.execute("""ALTER TABLE open.roadsItems
        ADD COLUMN {} integer""".format(cat))
    conn.commit()
    for cr in crimes2:
        mycurs.execute("""ALTER TABLE open.roadsItems
    ADD COLUMN {} integer""".format(cr))
    conn.commit()

def fillT():
    i=0
    while i< len(categories):
        mycurs.execute("""UPDATE open.roadsItems SET {0}= c from (
        SELECT distinct(r2.road_id) as r, count(distinct(venue_id)) as c
        FROM open.nyc_fs_venue_join r
            left join open.nyc_road2fs_near2 r2 on r2.fs_id=r.venue_id
            where parent_name={1} group by r2.road_id)
            as foo where foo.r=roadsItems.gid""".format(categories2[i], categories[i]))
        i+=1
    conn.commit()
    i=0
    while i< len(crimes):
        mycurs.execute("""UPDATE open.roadsItems SET {0}= c from (
          SELECT distinct(road_id) as r, count(distinct(object_id)) as c
        FROM open.nyc_road_proj_final r
            left join open.nyc_road2pi_5ft r2 on r2.road_id=r.gid
            where offense={1}  group by road_id)
            as foo where foo.r=roadsItems.gid""".format(crimes2[i], crimes[i]))
        i+=1
    conn.commit()


def stat():
    try:
        mycurs.execute("""DROP TABLE open.roadsItemsCorr""")
    except:
        print("table does not exist yet")
    mycurs.execute("""CREATE TABLE open.roadsItemsCorr (
    x varchar,
    y varchar,
    r_pearson numeric,
    p_pearson numeric,
    sig_pearson boolean,
    r_spearman numeric,
    p_spearman numeric,
    sig_spearman boolean
    )""")
    conn.commit()
    print("table created")

    listx=categories2+crimes2

    for x in listx:
        for y in listx:
            mycurs.execute("""SELECT gid, {0}, {1} from open.roadsItems
            where arts is not null and college is not null""".format(x, y))
            results=mycurs.fetchall()
            #print(results[1])

            lx=list()
            ly=list()
            for row in results:
                if row[1]==None:
                   itemx=0
                else: 
                    itemx=row[1]
                if row[2]==None:
                    itemy=0
                else:
                    itemy=row[2]
                if itemy==0 and itemx==0:
                    pass
                else:
                    lx.append(itemx)
                    ly.append(itemy)
            ax=np.array(lx)
            ay=np.array(ly)
            print(len(ax), len(ay))
            
            a=0.001
            result1=sc.pearsonr(ax, ay)
            print("Pearson r {0}, {1}: {2}".format(x, y, result1))
            if result1[1] <= a:
                sig1=True
            else:
                sig1=False

            result2=sc.spearmanr(ax, ay)
            print("Spearman r {0}, {1}:  {2}".format(x, y, result2))
            if result2[1] <= a:
                sig2=True
            else:
                sig2=False


            mycurs.execute("""Insert into open.roadsItemsCorr 
                (x, y, r_pearson, p_pearson, sig_pearson, r_spearman, p_spearman, sig_spearman) values
                ('{0}', '{1}', {2}, {3}, {4}, {5}, {6}, {7})"""
                .format(x, (y), result1[0], result1[1], sig1, result2[0], result2[1], sig2))
   
    conn.commit()


categories=["'Arts & Entertainment'", "'College & University'", "'Event'", "'Food'", "'Nightlife Spot'", "'Outdoors & Recreation'", "'Professional & Other Places'", "'Residence'", "'Shop & Service'", "'Travel & Transport'"]
crimes=["'ROBBERY'", "'GRAND LARCENY'", "'FELONY ASSAULT'", "'BURGLARY'", "'GRAND LARCENY OF MOTOR VEHICLE'"]
categories2=["Arts","College","Event","Food","NightlifeSpot","Outdoors","Professional","Residence","Shop","Travel"]
crimes2=["ROBBERY","GRANDLARCENY","FELONYASSAULT","BURGLARY","GRANDLARCENYOFMOTORVEHICLE"]

#createT()
#fillT()
stat()   
