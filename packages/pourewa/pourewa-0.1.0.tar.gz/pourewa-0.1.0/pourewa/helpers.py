import configparser
import os
import datetime


NAME = 'POUREWA'
## ====== CONFIG STUFF ====================================================================================
thisConfFileName = f'{NAME}.conf'
rootDir = os.path.abspath(os.path.dirname(__file__))


config = configparser.ConfigParser()

all_config_files = [os.path.join(rootDir,thisConfFileName), 
                    os.path.join(os.path.expanduser("~"),thisConfFileName),
                    os.path.join(os.path.expanduser("~"),'.'+thisConfFileName), 
                    os.path.join(os.path.expanduser("~"), '.config',thisConfFileName),
                    os.environ.get(f"{NAME}_CONF", '')]
    

config.read(all_config_files)


environment = config.get("app", "environment")
DEBUG = config.get("app", "debug")
LOG_FILE_NAME = config.get("app", "LOG_FILE_NAME")
#
ORTHANC_URL = config.get("app", "ORTHANC_URL")
ORTHANC_PORT = config.get("app", "ORTHANC_PORT")
ORTHANC_EXPOSED = config.get("app", "ORTHANC_EXPOSED")
ORTHANC_USERNAME = config.get("app", "ORTHANC_USERNAME")
ORTHANC_PASSWORD = config.get("app", "ORTHANC_PASSWORD")

# ------------------------------------------------------------------------------------------------------------



## ====== HELPER FUNCTIONS ====================================================================================

def dbDateToDateTime(dbDate):
    try:
        return datetime.datetime.strptime(dbDate, '%Y%m%d')
    except ValueError:
        return datetime.datetime.strptime(dbDate, '%Y%m%dT%H%M%S')

def fixPath(p):
    return p.encode('utf8', 'ignore').strip().decode()

def cleanString(ss):
    if not type(ss) == str:
        return ss
    ss = ss.replace('^', '-')
    ss = ss.replace(' ', '_')
    keepcharacters = ('-', '.', '_', 'ö','ü','ä','é','è','à')
    ss = "".join([c for c in ss if (c.isalnum() or (c.lower() in keepcharacters))]).rstrip()
    try:
        if ss[-1] == '.':
            ss = ss[:-1]
    except IndexError:
        pass
    # return ss
    return fixPath(ss)

def dateTimeToString(dt):
    return dt.strftime("%Y%m%d-%H:%M:%S")

def getDateNow():
    return dateTimeToString(datetime.datetime.now())

def countFilesInDir(dirName):
    files = []
    if os.path.isdir(dirName):
        for _, _, filenames in os.walk(dirName): 
            files.extend(filenames)
    return len(files)
# ------------------------------------------------------------------------------------------------------------



## ====== SET UP LOGGING ====================================================================================
try:
    LOG_FILE_NAME
except NameError:
    LOG_FILE_NAME = ''
if len(LOG_FILE_NAME) > 0:
    import logging
    if os.path.isfile(LOG_FILE_NAME):
        os.rename(LOG_FILE_NAME, f'{LOG_FILE_NAME[:-4]}_{getDateNow()}.log')
    logging.basicConfig(filename=LOG_FILE_NAME, 
                        filemode='w', 
                        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level='INFO')

    logging.info('Logfile set up')

# ------------------------------------------------------------------------------------------------------------


