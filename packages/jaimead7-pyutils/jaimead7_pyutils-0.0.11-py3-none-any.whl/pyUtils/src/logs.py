import logging
from datetime import datetime

from .config import cfg


class Styles:
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEBUG = '\033[94m'
    INFO = '\033[0m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    CRITICAL = '\033[101m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'

def _getLoggingLevel() -> int:
    try:
        return logging.__dict__[cfg.app.loggingLevel.upper()]
    except (KeyError, AttributeError):
        return logging.DEBUG

def setLoggingLevel(lvl: int = _getLoggingLevel()) -> int:
    logging.getLogger().setLevel(lvl)

logging.basicConfig(level= _getLoggingLevel(),
                    format= '%(message)s')

def debugLog(msg: str, style: Styles = Styles.DEBUG) -> None:
    logging.debug(f'{style}DEBUG -----> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}:{Styles.ENDC} {msg}')

def infoLog(msg: str, style: Styles = Styles.INFO) -> None:
    logging.info(f'{style}INFO ------> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}:{Styles.ENDC} {msg}')

def warningLog(msg: str, style: Styles = Styles.WARNING) -> None:
    logging.warning(f'{style}WARNING ---> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}:{Styles.ENDC} {msg}')

def errorLog(msg: str, style: Styles = Styles.ERROR) -> None:
    logging.error(f'{style}ERROR -----> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}:{Styles.ENDC} {msg}')

def criticalLog(msg: str, style: Styles = Styles.CRITICAL) -> None:
    logging.critical(f'{style}CRITICAL --> {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}:{Styles.ENDC} {msg}')
