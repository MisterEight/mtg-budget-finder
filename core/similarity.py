import os
import re
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from db.connection import connect

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

_PROJECTION = {
    "oracle_id": 1,
    "name": 1,
    "mana_cost": 1,
    "type_line": 1,
    "cmc": 1,
    "color_identity": 1,
    "oracle_text": 1,
    "prices": 1,
}


def _load_models():
    vectorizer = joblib.load(os.path.join(MODELS_DIR, "tfidf_model.pkl"))
    matrix = joblib.load(os.path.join(MODELS_DIR, "tfidf_matrix.pkl"))
    oracle_ids = joblib.load(os.path.join(MODELS_DIR, "tfidf_cards.pkl"))
    return vectorizer, matrix, oracle_ids


def _is_color_compatible(candidate_ci, query_ci):
    return set(candidate_ci).issubset(set(query_ci))


def _parse_price(prices):
    price_str = (prices or {}).get("usd")
    return float(price_str) if price_str else float("inf")


def find_alternatives(card_name, top_n=10, cmc_range=2, min_similarity=0.1):
    """
    Returns (query_card, alternatives) where alternatives is a list of dicts
    sorted by price ascending (cheapest first), pre-filtered to top_n by similarity.
    Returns (None, []) if the card is not found.
    """
    vectorizer, matrix, oracle_ids = _load_models()
    oracle_id_index = {oid: i for i, oid in enumerate(oracle_ids)}

    with connect() as collection:
        card = collection.find_one(
            {"name": {"$regex": f"^{re.escape(card_name)}$", "$options": "i"}},
            _PROJECTION,
        )

        if card is None:
            return None, []

        oracle_id = card["oracle_id"]
        color_identity = set(card.get("color_identity") or [])
        cmc = card.get("cmc") or 0

        if oracle_id not in oracle_id_index:
            return card, []

        card_idx = oracle_id_index[oracle_id]
        similarities = cosine_similarity(matrix[card_idx], matrix).flatten()

        # Map oracle_id -> similarity score, excluding the query card and low scores
        id_to_score = {
            oracle_ids[i]: float(similarities[i])
            for i in range(len(oracle_ids))
            if i != card_idx and similarities[i] >= min_similarity
        }

        if not id_to_score:
            return card, []

        candidate_docs = list(collection.find(
            {
                "oracle_id": {"$in": list(id_to_score.keys())},
                "cmc": {"$gte": cmc - cmc_range, "$lte": cmc + cmc_range},
            },
            _PROJECTION,
        ))

    # Filter by color identity: substitute must fit within the original's color identity
    results = []
    for doc in candidate_docs:
        if not _is_color_compatible(doc.get("color_identity") or [], color_identity):
            continue
        doc["_price"] = _parse_price(doc.get("prices"))
        doc["similarity"] = id_to_score[doc["oracle_id"]]
        results.append(doc)

    # Take top_n by similarity, then sort by price ascending
    results.sort(key=lambda c: c["similarity"], reverse=True)
    results = results[:top_n]
    results.sort(key=lambda c: c["_price"])

    return card, results
