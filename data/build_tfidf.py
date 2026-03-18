import os
import joblib
import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from core.config import MONGO_URI, DB_NAME, COLLECTION_NAME

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

def build():
    client = pymongo.MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION_NAME]

    cursor = collection.find(
        {"oracle_text": {"$exists": True, "$ne": ""}},
        {"oracle_id": 1, "oracle_text": 1}
    )
    cards = list(cursor)
    client.close()

    oracle_ids = [c["oracle_id"] for c in cards]
    texts = [c["oracle_text"] for c in cards]

    print(f"Treinando TF-IDF em {len(texts)} cartas...")
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(texts)

    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(vectorizer, os.path.join(MODELS_DIR, "tfidf_model.pkl"))
    joblib.dump(matrix,     os.path.join(MODELS_DIR, "tfidf_matrix.pkl"))
    joblib.dump(oracle_ids, os.path.join(MODELS_DIR, "tfidf_cards.pkl"))
    print("Modelos salvos em models/")

if __name__ == "__main__":
    build()
