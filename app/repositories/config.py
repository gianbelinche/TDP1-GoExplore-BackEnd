from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config.constants import DB_URL, DB_NAME, ENV_NAME
from app.config.logger import setup_logger
from pymongo_inmemory import MongoClient as MemoryMongoClient

logger = setup_logger(__name__)


def get_database():
    if ENV_NAME == 'TEST':
        conn = MemoryMongoClient()
        logger.info("Memory DB initialized")
        return conn[DB_NAME]
    else:
        conn = MongoClient(DB_URL, serverSelectionTimeoutMS=5000)

        try:
            conn.admin.command('ismaster')
            logger.info("Connection with DB established")
        except ConnectionFailure:
            logger.error("Server not available")
        return conn[DB_NAME]


db = get_database()


def clear_db():
    for name in db.list_collection_names():
        db.drop_collection(name)
