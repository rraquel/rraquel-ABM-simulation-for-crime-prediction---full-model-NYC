import os, sys, time, configparser
import logging
from Model import Model
import psycopg2, sys, os
from pandas import ExcelWriter


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

def writeExcel(agent_df,model_df):
    """Create xls for later analysis"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    excelfile = os.path.join(dir_path,'..','output','offender.{}.xls'.format(time.strftime('%Y%m%d_%H%M%S')))
    excelwriter = ExcelWriter(excelfile)
    model_df.to_excel(excelwriter,sheet_name='Model')
    agent_df.to_excel(excelwriter,sheet_name='Agent')
    excelwriter.close()


# Create model with it's street network, venues, agents, ...
def createModel():
    global model, config
    try: 
        modelCfg=config['model']
    except:
        log.error("Problem with config. section model")
        sys.exit(1)
    model=Model(modelCfg)

# Step through the model
def stepModel():
    global model, config
    #iterates for model steps
    i=0
    for i in range(config.getint('general','numSteps',fallback=1)):
        model.step(i, config.getint('general','numSteps'))
        print("=> step {0} performed".format(i))
    #statistics collection and data output
    #get data as pandas data frame
    agent_df = model.dc.get_agent_vars_dataframe()
    model_df = model.dc.get_model_vars_dataframe()
    writeExcel(agent_df,model_df)
    print(agent_df)
    log.info('Global stats: \n{}'.format(model_df.tail()))

# Initialize variables so they can be used as global
model=""
config=""

log=logging.getLogger('')

readConfig()
log.info("Config read")
print('start')
createModel()
print('model created')
stepModel()

print("end")