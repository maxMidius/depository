import logging
import logging.handlers
import coloredlogs
from icecream import ic
from contextlib import redirect_stdout
import sys

coloredlogs.install(level='DEBUG', fmt='%(asctime)s %(levelname)s %(message)s')

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create file handlers
# Create a console handler 
console_handler = logging.StreamHandler()
file_handler = logging.handlers.RotatingFileHandler('my_log.log', maxBytes=10240, backupCount=5)
file_handler1 = logging.handlers.RotatingFileHandler('logs/error.log', maxBytes=10240, backupCount=5)
file_handler2 = logging.handlers.RotatingFileHandler('logs/info.log', maxBytes=10240, backupCount=5)

console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.INFO)
file_handler1.setLevel(logging.ERROR)
file_handler2.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(file_handler1)
logger.addHandler(file_handler2)

# Use the logger to log messages
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')


# Create a console handler
console_handler.setLevel(logging.DEBUG)

# Configure your logger
logging.basicConfig(level=logging.DEBUG)

# Customize IceCream's output function
def custom_output_function(s):
    logger.debug(s)


ic.configureOutput(outputFunction=custom_output_function)

# Now, use ic() as usual
x = 10
ic(x)     




