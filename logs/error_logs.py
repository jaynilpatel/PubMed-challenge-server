import logging

LOG_FILENAME = "logs"
logging.basicConfig(filename=LOG_FILENAME,format='%(asctime)s %(message)s', filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)