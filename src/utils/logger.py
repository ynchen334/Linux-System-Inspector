import logging
from logging.handlers import RotatingFileHandler

def setup_logger(level=logging.INFO):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    if not logger.handlers:
        fh = RotatingFileHandler(
            filename="logs/inspector.log", 
            maxBytes=1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        fmt = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s",    
            datefmt = "%Y/%m/%d %H:%M:%S"
        )
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger
