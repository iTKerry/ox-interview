from flask import jsonify, request

from app.embeddings import generate_embedding
from app.storage import add_to_index, search_similar

def health_check():
    return jsonify(status="healthy"), 200

def add_text():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify(error="No text provided"), 400

    embedding = generate_embedding(text)
    text_id = add_to_index(embedding, text)

    return jsonify(status="success", id=text_id), 200

def find_similar():
    if not request.is_json:
        return jsonify(error="No text provided"), 400

    data = request.get_json(silent=True)
    if not data or 'text' not in data:
        return jsonify(error="No text provided"), 400

    text = data.get('text', '')
    n = data.get('n', 5)

    if not text:
        return jsonify(error="No text provided"), 400

    embedding = generate_embedding(text)
    results = search_similar(embedding, n)

    return jsonify(results=results), 200