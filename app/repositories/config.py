from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config.constants import DB_URL, DB_NAME
from app.config.logger import setup_logger

conn = MongoClient(DB_URL, serverSelectionTimeoutMS=5000)
logger = setup_logger(__name__)

try:
    conn.admin.command('ismaster')
    logger.info("Connection with DB established")
except ConnectionFailure:
    logger.error("Server not available")

db = conn[DB_NAME]
