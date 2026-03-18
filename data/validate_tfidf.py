import joblib
import os

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

ids    = joblib.load(os.path.join(MODELS_DIR, "tfidf_cards.pkl"))
matrix = joblib.load(os.path.join(MODELS_DIR, "tfidf_matrix.pkl"))
model  = joblib.load(os.path.join(MODELS_DIR, "tfidf_model.pkl"))

print(f"Cartas indexadas : {len(ids)}")
print(f"Shape da matriz  : {matrix.shape}")
print(f"Vocabulário      : {len(model.vocabulary_)} termos")
print(f"Exemplo de ID    : {ids[0]}")
