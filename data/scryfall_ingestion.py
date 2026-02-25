import os
import requests
import pymongo

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "mtg_budget_finder")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "cards")

BULK_DATA_URL = "https://api.scryfall.com/bulk-data"

def get_bulk_data_url():
    response = requests.get(BULK_DATA_URL)
    response.raise_for_status()
    bulk_data = response.json()

    for item in bulk_data["data"]:
        if item["type"] == "oracle_cards":
            return item["download_uri"]

    raise ValueError("Bulk data oracle_cards não encontrado")

def download_cards(download_uri):
    # TODO: usar streaming para evitar carregar ~200MB inteiros na memória
    print("Baixando cartas...")
    response = requests.get(download_uri)
    response.raise_for_status()
    return response.json()

def save_to_mongo(cards):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    collection.drop()  # TODO: adicionar confirmação antes de dropar em produção
    print(f"Inserindo {len(cards)} cartas no MongoDB...")
    collection.insert_many(cards)

    # TODO: criar índices em name, keywords e type_line para buscas eficientes
    print("Ingestão concluída.")
    client.close()

if __name__ == "__main__":
    download_uri = get_bulk_data_url()
    cards = download_cards(download_uri)
    save_to_mongo(cards)