from termcolor import colored
import logging

#######################################################################################################################################
# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

COLORS = {
    'WARNING': 'yellow',
    'INFO': 'white',
    'DEBUG': 'blue',
    'CRITICAL': 'red',
    'ERROR': 'red'
}

class DebugModuleFilter(logging.Filter):
    def __init__(self):
        logging.Filter.__init__(self)
        self.debug_modules = set([])

    def filter(self, record):
        if record.levelno == logging.DEBUG:
            return record.name[:3]=='sad'
        return True

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, datefmt=None):
        logging.Formatter.__init__(self, msg, datefmt=datefmt)

    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS:
            record.levelname = colored(levelname, COLORS[levelname])
        return logging.Formatter.format(self, record)

class ColoredLogger(logging.Logger):
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)                

        self.addFilter(DebugModuleFilter())

        color_formatter = ColoredFormatter(
            msg = colored("%(asctime)s","magenta") + "[%(levelname)s] %(message)s" + colored(" %(name)s %(filename)s:%(lineno)d", 'white', attrs=['dark']),
            datefmt='%d.%m %H:%M:%S', # datefmt='%d.%m.%Y %I:%M:%S',
            )

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)

logging.setLoggerClass(ColoredLogger)
logger = logging.getLogger(__name__)
# logger.info("Start logging") # Do not uncomment. The line prevents change of the log level.

