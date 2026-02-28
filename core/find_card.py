import pymongo
from core.config import MONGO_URI, DB_NAME, COLLECTION_NAME

def connect_mongo():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    return client, collection

def search_card(name, collection):
    card_information = collection.find_one({"name": {"$regex": name, "$options": "i"}})
    return card_information

if __name__ == "__main__":
    client, collection = connect_mongo()
    card_name = input("Digite o nome da carta:")
    card_information = search_card(card_name, collection)

    if card_information:
        print(card_information)
    else:
        print("Carta não encontrada.")

    client.close()