import sys
import logging
from loguru import logger
from .config import settings

class InterceptHandler(logging.Handler):
    """
    Standard Library Logging Interceptor.
    Redirects standard logging architecture to Loguru for consistent JSON output.
    """
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def setup_logging():
    """
    Configure Loguru for Production.
    - JSON serialization for machine parsing (Splunk/ELK).
    - Intercepts Uvicorn/FastAPI logs.
    """
    # Remove default handlers
    logger.remove()
    
    # Determine format: JSON for prod, colored text for dev
    if settings.ENVIRONMENT == "production":
        logger.add(
            sys.stderr,
            level=settings.LOG_LEVEL,
            serialize=True, # JSON Format
            backtrace=False,
            diagnose=False,
        )
    else:
        logger.add(
            sys.stderr,
            level=settings.LOG_LEVEL,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            colorize=True
        )

    # Intercept standard library usage
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    for log_name in ("uvicorn", "uvicorn.access", "fastapi"):
        logging_logger = logging.getLogger(log_name)
        logging_logger.handlers = [InterceptHandler()]

    return logger

setup_logging()
