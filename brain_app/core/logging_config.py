import logging
import sys

def setup_logging():
    logger = logging.getLogger("brain_app")
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger

logger = setup_logging()
