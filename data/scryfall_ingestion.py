import requests
import ijson
from db.connection import connect

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
    print("Baixando cartas...")
    response = requests.get(download_uri, stream=True)
    response.raise_for_status()
    response.raw.decode_content = True
    return list(ijson.items(response.raw, "item", use_float=True))

def save_to_mongo(cards):
    with connect() as collection:
        collection.drop()  # TODO: adicionar confirmação antes de dropar em produção
        print(f"Inserindo {len(cards)} cartas no MongoDB...")
        collection.insert_many(cards)
        collection.create_index("name")
        collection.create_index("keywords")
        collection.create_index("type_line")
        print("Ingestão concluída.")

if __name__ == "__main__":
    download_uri = get_bulk_data_url()
    cards = download_cards(download_uri)
    save_to_mongo(cards)