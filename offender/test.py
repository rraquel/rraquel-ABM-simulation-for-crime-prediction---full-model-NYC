import Model
import random
import sys, psycopg2, os, time, random, logging
import networkx as nx
from random import choices
from pandas import DataFrame



def connectDB():
        try:
            conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
            curs=conn.cursor()
            logging.info("connected to DB")
        except Exception as e:
            logging.debug("not connected")
        return conn

def createRoadNetwork():
        # SQL to select data
        # from intersection2road table as i2r: intersection_id [key]
        # from open.nyc_road_proj_final as r: gid [1]
        # from open.nyc_road_attributes as ra: length [2], crimes_2015 [3]
        # join tables using road_id into gid
        totalCrimes=0
        roadLength=0
        #crimes_2015: n crime to 1 road mapping
        
        curs.execute("""select intersection_id,r.gid,length,crimes_2015 from 
            open.nyc_intersection2road i2r
            left join open.nyc_road_proj_final r on i2r.road_id = r. gid
            left join open.nyc_road_attributes ra on ra.road_id=r.gid""")
        #fetch all values into tuple
        interRoad=curs.fetchall()
        #dictionary {} -  a Key and a value, in this case a key and a set() of values -unordered collection
        intersect={}
        G=nx.Graph()
        #for each line in interRoad 
        for line in interRoad:
            #if attribute[0] (intersection_id) is not in intersect
            if not line[0] in intersect:
                #initialize a set for the key (intersect_id)
                intersect[line[0]]=set()
            #add current road_id to key
            intersect[line[0]].add(line[1])
            totalCrimes+=line[3]
            #add road, length and crimes as node info in graph
            #self.G.add_node(line[1], length=line[2], num_crimes=line[3])
            # TODO Parameter: Assumptions Humans walk 300 feet in 60s
            G.add_node(line[1],length=line[2],num_crimes=line[3],crimesList=set())
            #self.G.node[line[1]]['crimesList'].add(line[3])
            roadLength+=line[2]
        #build edges with information on nodes (roads)
        # loops over each intersection in intersect[]     
        for interKey in intersect.keys():
            #loops over each road in the current intersection
            for road in intersect[interKey]:
                #loops over roads again to compare roads and map relationship
                for road2 in intersect[interKey]:
                    if not road==road2:
                        G.add_edge(road, road2)
        return G

print('start')
totalCrimes=0
count=100
Resultingweights=[]
ResultingVenues=[]
conn=connectDB()
curs = conn.cursor()

G=createRoadNetwork()
print('start')

while count is not 0:
    road=random.sample(G.nodes(),1)[0]
    count-=1
    curs.execute("""SELECT venue_id, road_id, weight_center, checkins_count, weighted_checkins FROM(
    SELECT venue_id, weight_center, checkins_count,(checkins_count * 100.0)/temp.total_checkins as weighted_checkins
    from (SELECT COUNT(venue_id)as total_venues, SUM(checkins_count) as total_checkins FROM open.nyc_fs_venue_join
    where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
    and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2})
    ) as temp, open.nyc_fs_venue_join_weight_to_center
    where st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {1})
    and not st_dwithin((select geom from open.nyc_road_proj_final where gid={0}),ftus_coord, {2}))
    AS fs LEFT JOIN open.nyc_road2fs_80ft r2f on r2f.location_id=fs.venue_id WHERE NOT road_id is null"""
    .format(road,41000,40000))
    venues=curs.fetchall() #returns tuple of tuples, venue_id,weighted_checkins
    #venueId=random.choice(venues) #selects a random element of the tuple
    #for random.choices weights= need a list of the weights - therefore convert weights to list using list comprehension
    weight1=[x[2] for x in venues]
    weight2=[x[4] for x in venues]
    #convert decimal.Decimal to float
    weight2=[float(i) for i in weight2]
    combinedWeights=[i*j for i,j in zip(weight1,weight2)]
    #print('combined weights: {}'.format(combinedWeights[0]))
    #convert float to integer
    #weightsListInt = list(map(int, combinedWeights))
    venue=choices(venues, weights=combinedWeights, k=1)
    #print('venue: {}'.format(venue))
    venueId=venue[0][0]
    roadId=venue[0][1]
    ResultingVenues.append(venue[0])
    Resultingweights.append(combinedWeights)
df = DataFrame({'weights list': Resultingweights, 'Resulting venues': ResultingVenues})
df.to_excel('test.xlsx', sheet_name='sheet1', index=False)
print('resulting weights: {}'.format(Resultingweights))