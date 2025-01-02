import faiss
import numpy as np



# TODO: WARNING clustering 100 points to 100 centroids: please provide at least 3900 training points
class FAISSStorage:
    def __init__(self, dimension=384, nlist=100):
        self.dimension = dimension
        self.nlist = nlist
        self.quantizer = faiss.IndexFlatL2(self.dimension)
        self.index = faiss.IndexIVFFlat(self.quantizer, self.dimension, self.nlist, faiss.METRIC_L2)
        self.index.nprobe = 10
        self.texts = []
        self.pending_embeddings = []
        self.is_trained = False

    def add_to_index(self, embedding, text):
        self.texts.append(text)
        self.pending_embeddings.append(embedding)

        if not self.is_trained and len(self.pending_embeddings) >= 100:
            self.train_index()

        if self.is_trained:
            self.index.add(np.array([embedding]))

    def train_index(self):
        if len(self.pending_embeddings) < 100:
            raise ValueError("Not enough data to train the index. At least 100 embeddings are required.")

        embeddings = np.array(self.pending_embeddings)
        try:
            self.index.train(embeddings)
            self.index.add(embeddings)
            self.pending_embeddings = []
            self.is_trained = True
            print(f"Training completed successfully. is_trained={self.is_trained}")
        except Exception as e:
            print(f"Error during FAISS training: {e}")
            raise ValueError("FAISS training failed.")

    def search_similar(self, query_embedding, n=5):
        if not self.is_trained:
            raise ValueError("FAISS index is not trained. Cannot perform search.")

        distances, indices = self.index.search(np.array([query_embedding]), n)
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.texts):
                results.append({
                    "text": self.texts[idx],
                    "similarity": float(1 - distances[0][i])
                })
        return results

faiss_storage = FAISSStorage()