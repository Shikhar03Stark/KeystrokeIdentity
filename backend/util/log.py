import logging
from util.config import get_env

def _init_logger():
    logger = logging.getLogger(__name__)
    env = get_env()
    logger.setLevel(logging.DEBUG if env == 'dev' else logging.INFO)
    return logger

_logger = None

def info(msg):
    global _logger
    if _logger is None:
        _logger = _init_logger()
    _logger.info(msg)
    
def debug(msg):
    global _logger
    if _logger is None:
        _logger = _init_logger()
    _logger.debug(msg)
    
def error(msg):
    global _logger
    if _logger is None:
        _logger = _init_logger()
    _logger.error(msg)