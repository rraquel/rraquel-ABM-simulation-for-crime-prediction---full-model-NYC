import os, sys, time, configparser
import logging
from Model import Model
import psycopg2, sys, os


# Read the supplied config file or default config if none is supplied
def readConfig():
    """Find config file and read it"""
    #global variable
    global config
    #directory of current file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if len(sys.argv) > 1:
        #config folder and file
        cfile = os.path.join(dir_path,'..','config',sys.argv[1])
    else:
        cfile = os.path.join(dir_path,'..','config','default.ini')
    config = configparser.ConfigParser()
    config.read(cfile)

# Create model with it's street network, venues, agents, ...
def createModel():
    global model, config
    try: 
        modelCfg=config['model']
    except:
        logging.getLogger().error("Problem with config. section model")
        sys.exit(1)
    model=Model(modelCfg)

# Step through the model
def stepModel():
    global model, config
    for i in range(15):
        model.step()
        print("=> step {0} performed".format(i))
        logging.getLogger().info("===> Performed step {0} in {1}s".format(i,time.monotonic()-t))

# Initialize variables so they can be used as global
model=""
config=""

readConfig()
logging.getLogger().info("Config read")
print('start')
createModel()
print('model created')
stepModel()

print("end")