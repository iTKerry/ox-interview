from app.embeddings import generate_embedding

def test_generate_embedding():
    text = "This is a test."
    embedding = generate_embedding(text)
    assert len(embedding) == 384
