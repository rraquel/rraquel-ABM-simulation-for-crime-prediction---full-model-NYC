import networkx as nx
import psycopg2, sys, os, time, random, logging
import globalVar

conn= psycopg2.connect("dbname='shared' user='rraquel' host='127.0.0.1' password='Mobil4b' ")
mycurs=conn.cursor()

roadLength=0
#crimes_2015: n crime to 1 road mapping
#open.nyc_road_attributes without and open.nyc_road_attributes2 with census tract for each road
mycurs.execute("""select intersection_id,r.gid,length,crimes_2015, censustract from 
    open.nyc_intersection2road i2r
    left join open.nyc_road_proj_final r on i2r.road_id = r. gid
    left join open.nyc_road_attributes2 ra on ra.road_id=r.gid""")
#fetch all values into tuple
interRoad=mycurs.fetchall()
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

    G.add_node(line[1],length=line[2],census=line[4])  
for interKey in intersect.keys():
    #loops over each road in the current intersection
    for road in intersect[interKey]:
        #loops over roads again to compare roads and map relationship
        for road2 in intersect[interKey]:
            if not road==road2:
                G.add_edge(road, road2)
print("Number of  G: roads: {0}, intersections: {1}".format(G.number_of_nodes(), G.number_of_edges))

mycurs.execute("""select * from open.nyc_road_proj_final_isolates""")
#fetch all values into tuple
globalVar.isolateRoadsRNW.update(mycurs.fetchall())
#output is not a list of roads, but list of ('road_id')

print("node attributes {}".format(nx.get_node_attributes(G, 35068)))
print(G.neighbors(35068))
print("done")
road=61202
road=7
targetroad=35068
way=nx.shortest_path(G,road,targetroad,weight='length')
print(way)