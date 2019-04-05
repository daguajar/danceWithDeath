import logging
import os
from datetime import datetime

if not os.path.exists("logs"):
    os.makedirs("logs")

now = str(datetime.now()).split(".")[0].replace("-","").replace(":","").replace(" ","")
fileName = "logs/{0}.log".format(now)

ch = logging.FileHandler(fileName)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)

def createLog(name):

	logger = logging.getLogger(name)

	logger.setLevel(logging.DEBUG)
	logger.addHandler(ch)

	return logger