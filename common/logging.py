from logging import getLogger, basicConfig, StreamHandler, Formatter, captureWarnings
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from coloredlogs import ColoredFormatter

from common.config import Config

LOGGING_LEVELS = {'CRITICAL': CRITICAL,
                  'ERROR': ERROR,
                  'WARNING': WARNING,
                  'INFO': INFO,
                  'DEBUG': DEBUG,
                  'NOTSET': NOTSET}

LEVEL_STYLES = dict(spam=dict(color='green', faint=True),
                    debug=dict(faint=True),
                    verbose=dict(color='blue'),
                    info=dict(),
                    notice=dict(color='magenta'),
                    warning=dict(color='yellow'),
                    success=dict(color='green', bold=True),
                    error=dict(color='red'),
                    critical=dict(color='red', bold=True))

basicConfig(level=INFO)

captureWarnings(True)

consoleHeader = StreamHandler()
consoleHeader.setFormatter(
                Formatter(fmt='[%(asctime)-11s] %(levelname)-8s %(name)s.%(funcName)s: %(message)s',
                            datefmt='%d-%m-%y %H:%M:%S'))

def getCustomLogger(name):
    logger = getLogger(name)
    logger.setLevel(LOGGING_LEVELS.get(Config.LOGGING_LEVEL))
    logger.addHandler(consoleHeader)
    logger.propagate = False
    return logger

if Config.LOGGING_LEVEL in LOGGING_LEVELS.keys():
    basicConfig(level=LOGGING_LEVELS.get(Config.LOGGING_LEVEL))
    logger = getCustomLogger(__name__)
else:
    old_value = Config.LOGGING_LEVEL
    Config.LOGGING_LEVEL = 'INFO'
    logger = getCustomLogger(__name__)
    logger.warning(f'LOGGING_LEVEL={old_value} is ambiguous!')
    logger.info(f'Setting logging level to INFO!')

if Config.COLORED_LOGGING == 'True':
    consoleHeader.setFormatter(
        ColoredFormatter(fmt='[%(asctime)-11s] %(levelname)-8s %(name)s.%(funcName)s: %(message)s',
                        datefmt='%d-%m-%y %H:%M:%S',
                        level_styles=LEVEL_STYLES))
    logger.debug(f'Colored logging enabled!')
elif Config.COLORED_LOGGING == 'False':
    logger.debug(f'Disabling colored logging!')
else:
    logger.warning(f'COLORED_LOGGING={Config.COLORED_LOGGING} is ambiguous!')
    Config.COLORED_LOGGING = 'False'
    logger.info(f'Disabling colored logging!')

uvicorn_error_logger = getLogger("uvicorn.error")
uvicorn_error_logger.handlers.clear()
uvicorn_error_logger.addHandler(consoleHeader)
uvicorn_error_logger.propagate = False

uvicorn_access_logger = getLogger("uvicorn.access")
uvicorn_access_logger.handlers.clear()
uvicorn_access_logger.addHandler(consoleHeader)

warnings_logger = getLogger("py.warnings")
warnings_logger.propagate = False
warnings_logger.addHandler(consoleHeader)