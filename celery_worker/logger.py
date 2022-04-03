import os
import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <5}</level> | <magenta>{process}</magenta> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>')

logfile = os.environ.get("SAFETY_PING_LOGFILE", None)
if logfile:
    logger.add(logfile, serialize=True, rotation="40 MB")
