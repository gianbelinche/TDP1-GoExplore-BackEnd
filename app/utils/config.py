from app.config.constants import PORT, DB_URL
from app.config.logger import setup_logger

# TODO: Ver si esto es correcto
logger = setup_logger(name=__name__)


def log_config():
    logger.info("Configuration: ")
    logger.info(f"  - PORT: {PORT}")
    logger.info(f"  - DB_URL: {DB_URL}")
