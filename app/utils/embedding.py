from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    """
    Converts list of texts into embeddings
    """
    return model.encode(texts)

def cosine_similarity(a, b):
    """
    Measures similarity between two vectors
    """
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return np.dot(a, b)
