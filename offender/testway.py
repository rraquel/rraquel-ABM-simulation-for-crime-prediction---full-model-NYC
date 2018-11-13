import networkx as nx
import psycopg2, sys, os, time, random, logging
import globalVar

conn= psycopg2.connect("dbname='shared' user='rraquel' host='127.0.0.1' password='Mobil4b' ")
mycurs=conn.cursor()

G=nx.Graph()
G2=nx.Graph()

roads=dict()
intersect=dict()
roadLength=0
weightdict=dict()
#crimes_2015: n crime to 1 road mapping
#open.nyc_road_attributes without and open.nyc_road_attributes2 with census tract for each road
mycurs.execute("""select intersection_id,r.gid, length, ra.st_width, roadtypew, crimes_2015, censustract from 
    open.nyc_intersection2road i2r
    left join open.nyc_road_proj_final r on i2r.road_id = r. gid
    left join open.nyc_road_attributes2 ra on ra.road_id=r.gid""")
# total attributes: 148466 roads; st_width=0 '6061' --> 4%
#fetch all values into tuple
interRoad=mycurs.fetchall()
#dictionary {} -  a Key and a value, in this case a key and a set() of values -unordered collection

#for each line in interRoad 
for line in interRoad:
    #if attribute[0] (intersection_id) is not in intersect
    if not line[0] in intersect:
        #initialize a set for the key (intersect_id)
        intersect[line[0]]=set()
    #add current road_id to key
    intersect[line[0]].add(line[1])
#for G2
for line in interRoad:
    if not line[1] in roads:
        roads[line[1]]=set()
    roads[line[1]].add(line[0])            
    #add road, length and crimes as node info in graph
    #G.add_node(line[1], length=line[2], num_crimes=line[3])
    # TODO Parameter: Assumptions Humans walk 300 feet in 60s
    G.add_node(line[1],length=line[2], width=line[3], roadtype=line[4], census=line[6])
    G2.add_node(line[0])
    weightdict[line[1]]=[line[2], line[3], line[4], line[6]]
#for r in G.nodes_iter():
    #roadLength+=G.node[r]['length']
#log.debug("Found {} intersections".format(len(intersect)))
#log.debug("roadlenght: {}".format(roadLength))
#build edges with information on nodes (roads)
# loops over each intersection in intersect[]     
for interKey in intersect.keys():
    #loops over each road in the current intersection
    for road in intersect[interKey]:
        #loops over roads again to compare roads and map relationship
        for road2 in intersect[interKey]:
            if not road==road2:
                G.add_edge(road, road2)
#for G2
for roadKey in roads.keys():
    #loop over each intersection in roads
    for inters in roads[roadKey]:
        #loop over intersection again to compare intersect and map relationship
        for inters2 in roads[roadKey]:
            if not inters==inters2:
                G2.add_edge(inters, inters2, length=weightdict[roadKey][0], width=weightdict[roadKey][1], lengthwidth=((10*weightdict[roadKey][0])*weightdict[roadKey][1]), roadtype=weightdict[roadKey][2], roadtypelength=(weightdict[roadKey][0]*weightdict[roadKey][2]), census=weightdict[roadKey][3])

#print("Number of  G: roads: {0}, intersections: {1}".format(G.number_of_nodes(), G.number_of_edges))
#print("Number of  G2: roads: {1}, intersections: {0}".format(G2.number_of_nodes(), G2.number_of_edges))
#log.debug("Isolated roads: {0}".format(len(nx.isolates(G))))
#log.info("roadNW built, intersection size: {0}".format(len(intersect)))
#log.info("roadNW built, roads size: {0}".format(G.number_of_nodes()))


"""      
117320	total	100%
115694	minus isolates	98.61%
113182	minus detached	96.47%
"""
mycurs.execute("""select * from open.nyc_road_proj_final_isolates""")
#fetch all values into tuple
globalVar.isolateRoadsRNW.update(mycurs.fetchall())


road=115425
targetroad=43681

if targetroad in globalVar.isolateRoadsRNW:
    print("targetroad in isolates")
elif road in globalVar.isolateRoadsRNW:
    print("road in isolates")

roadNode=random.choice(list(roads[road]))
targetNode=random.choice(list(roads[targetroad]))
if roadNode==targetNode:
    way=[road, targetroad]
    print("targetNode and roadNode are the same")
else:
    wayN=nx.shortest_path(G2,roadNode,targetNode, weight='length')

    print("start")
    i=0
    way=list()
    while i<len(wayN)-1:
        rl1=set(intersect[wayN[i]])
        rl2=set(intersect[wayN[i+1]])
        r=rl1.intersection(rl2)
        #road needs to be first road
        way.append(list(r)[0])
        i+=1
    print(way)
    #print("print roads in way {}".format(way))
    count=0
    #fix beginning and end of way
    l=len(way)
    print(l)
    r0=list()
    for r in way[:3]:
        r0.append(r)
        print(r, r0)
    rn=list()
    for r in way[-3:]:
        rn.append(r)
        print(r, rn)


    #START: self road is within 3 first roads, remove rest
    #print(road, r0, r1, r2)
    if road in r0:
        for r in r0:
            if r==road:
                break
            else:
                way.remove(r)
    else:
        #print("else")
        way1=nx.shortest_path(G,road,r0[0])
        #will give start and end road if they are the only ones in path
        print(way1)
        way1.pop()
        way=way1+way
    #print(way)
    #print("end")
    #print(targetroad, rn2, rn1, rn0)
    if targetroad in rn:
        for r in rn:
            #print("for")
            #print(r, targetroad)
            if r==targetroad:
                #print("f: if")
                break
            else:
                #print("f: else")
                way.remove(r)
    else:
        #print("else")
        print(rn)
        way2=nx.shortest_path(G,rn[-1], targetroad)
        print(way2)
        del way2[0]
        print(way2)
        way=way+way2
print(way)
print("way works number of roads {}".format(len(way)))
