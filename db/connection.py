from contextlib import contextmanager
import pymongo
from core.config import MONGO_URI, DB_NAME, COLLECTION_NAME


@contextmanager
def connect():
    client = pymongo.MongoClient(MONGO_URI)
    try:
        yield client[DB_NAME][COLLECTION_NAME]
    finally:
        client.close()
