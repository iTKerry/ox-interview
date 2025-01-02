import pytest

from app.storage import FAISSStorage
from app.embeddings import generate_embedding



@pytest.fixture
def storage():
    return FAISSStorage()


def test_train_threshold(storage):
    for i in range(99):
        embedding = generate_embedding(f"Test text {i}")
        storage.add_to_index(embedding, f"Test text {i}")

    assert not storage.is_trained, f"FAISS index should not be trained yet. Current state: {storage.is_trained}"

    embedding = generate_embedding("Trigger training")
    storage.add_to_index(embedding, "Trigger training")

    assert storage.is_trained, f"FAISS index should be trained after 100 texts. Current state: {storage.is_trained}"


def test_add_more_than_threshold(storage):
    for i in range(100):
        embedding = generate_embedding(f"Test text {i}")
        storage.add_to_index(embedding, f"Test text {i}")

    assert storage.is_trained, f"FAISS index should be trained after 100 texts. Current state: {storage.is_trained}"

    for i in range(10):
        embedding = generate_embedding(f"Extra text {i}")
        storage.add_to_index(embedding, f"Extra text {i}")

    assert len(storage.texts) == 110, f"All texts should be added successfully. Current text count: {len(storage.texts)}"
