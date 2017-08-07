import mesa
from mesa.time import RandomActivation
import networkx as nx
import sys, psycopg2, os, time, random, logging

class Agent(mesa.Agent):
    """an Agent moving"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.log=logging.getLogger('')
    
    def step(self):
        """step: behavior for each offender"""
        print('step done for agent ')
        