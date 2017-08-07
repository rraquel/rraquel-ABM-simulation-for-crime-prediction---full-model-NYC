import mesa
from Agent import Agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import networkx as nx
import psycopg2, sys, os, time, random, logging

class Model(mesa.Model):
    """ characteristics of the model."""
    def __init__(self):
        self.log=logging.getLogger('')
        self.num_agents=10
        self.schedule=RandomActivation(self)
        
        self.totalCrimes=0

        self.connectDB()
        self.log.info('Generating Model')

        #collect statistics from peragent&step (can be more)
        self.dc=DataCollector(model_reporters={} , agent_reporters={})

        #create roadNW
        self.createRoadNetwork()
        
        #create agent
        for i in range(self.num_agents):
            a=Agent(i, self)
            self.schedule.add(a)
            self.log.info("Offender created")

    def connectDB(self):
        try:
            self.conn= psycopg2.connect("dbname='shared' user='rraquel' host='localhost' password='Mobil4b' ")        
            self.curs=self.conn.cursor()
        except Exception as e:
            self.log.error("connection to DB failed"+str(e))
            sys.exit(1)
    
    def createRoadNetwork(self):
        # SQL to select data
        # from intersection2road table as i2r: intersection_id [key]
        # from open.nyc_road_proj_final as r: gid [1]
        # from open.nyc_road_attributes as ra: length [2], crimes_2015 [3]
        # join tables using road_id into gid
        self.curs.execute("""select intersection_id,r.gid,length,crimes_2015 from 
            open.nyc_intersection2road i2r
            left join open.nyc_road_proj_final r on i2r.road_id = r. gid
            left join open.nyc_road_attributes ra on ra.road_id=r.gid""")
        #fetch all values into tuple
        interRoad=self.curs.fetchall()
        #dictionary {} -  a Key and a value, in this case a key and a set() of values -unordered collection
        intersect={}
        self.G=nx.Graph()
        #for each line in interRoad 
        for line in interRoad:
            #if attribute[0] (intersection_id) is not in intersect
            if not line[0] in intersect:
                #initialize a set for the key (intersect_id)
                intersect[line[0]]=set()
            #add current road_id to key
            intersect[line[0]].add(line[1])
            self.totalCrimes+=line[3]
            #add road, length and crimes as node info in graph
            self.G.add_node(line[1], length=line[2], num_crimes=line[3])
        self.log.debug("Found {} intersections".format(len(intersect)))
        #build edges with information on nodes (roads)
        # loops over each intersection in intersect[]     
        for interKey in intersect.keys():
            #loops over each road in the current intersection
            for road in intersect[interKey]:
                #loops over roads again to compare roads and map relationship
                for road2 in intersect[interKey]:
                    if not road==road2:
                        self.G.add_edge(road, road2)
        self.log.debug("Length of  G: roads: {0}, intersections: {1}".format(self.G.number_of_nodes(), self.G.number_of_edges))
        self.log.debug("Isolated roads: {0}".format(len(nx.isolates(self.G))))
        print('roadNW built, intersection size: {0}'.format(len(intersect)))
        print('roadNW built, roads size: {0}'.format(self.G.number_of_nodes()))

    def step(self):
        """advance model by one step."""
        self.dc.collect(self)
        self.schedule.step()