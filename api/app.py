from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

@app.route('/health-check', methods=['GET'])
def health_check():
    return jsonify(status="healthy"), 200

@app.route('/test-embedding', methods=['POST'])
def test_embedding():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify(error="No text provided"), 400

    embedding = model.encode(text).tolist()
    return jsonify(embedding=embedding), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
