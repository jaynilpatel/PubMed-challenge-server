import os
import logging.config

basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
logging.config.fileConfig('%s/logging.conf' % basepath)
logger = logging.getLogger(__name__)