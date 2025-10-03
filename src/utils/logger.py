import logging
import os
from datetime import datetime
# Get the absolute path of the directory containing the current script.
relative_path = 'src/data/events.db'

logging.basicConfig(filename=relative_path, level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is when this event was logged.')
logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")  + ' - Program started')
logging.shutdown()