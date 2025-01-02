import faiss
from numpy import array

dimension = 384
index = faiss.IndexFlatL2(dimension)
texts = []

def add_to_index(embedding, text):
    index.add(array([embedding]))
    texts.append(text)
    return len(texts) - 1

def search_similar(query_embedding, n):
    if len(texts) == 0:
        return []
    distances, indices = index.search(array([query_embedding]), n)
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(texts):
            results.append({
                "text": texts[idx],
                "similarity": float(1 - distances[0][i])  # Convert distance to similarity
            })
    return results
