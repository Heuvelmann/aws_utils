import logging
import sys
from datetime import datetime


### Standar Output Handler

logger_app_name = "Utils_modulo"
logger = logging.getLogger(logger_app_name)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

consoleHandle = logging.StreamHandler(sys.stdout)
consoleHandle.setLevel(logging.INFO)
consoleHandle.setFormatter(formatter)
logger.addHandler(consoleHandle)
### Logconfig

#logger_app_name = 
#log_file_name = datetime.now().strftime('datalakelogs_%H_%M_%d_%m_%Y.log')




### File Handler

#filehandler = logging.FileHandler(log_file_name)
#filehandler.setLevel(logging.INFO)
#filehandler.setFormatter(formatter)

#logger.addHandler(filehandler)


