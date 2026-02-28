import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "mtg_budget_finder")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "cards")
