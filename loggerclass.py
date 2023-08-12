import os
import logging
import datetime

def getLogger(name): 
    script_directory = os.path.dirname(os.path.abspath(__file__))
    logger = logging.Logger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(os.path.join(script_directory+'/'+'logging_info_'+str(datetime.date.today())+'.log'), 'a')
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger