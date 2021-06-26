import logging
from typing import Callable, Optional

logger = logging.getLogger('__main__')

logger.setLevel(level=logging.DEBUG)
fh = logging.FileHandler('log.log')
fh_formatter = logging.Formatter('[%(levelname)s] - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

def print_and_log(message, level: Optional[Callable] = None, end: str = None):
    if level:
        level(message)
    else:
        logger.info(message)
    print(message, end=end)