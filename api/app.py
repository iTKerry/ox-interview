from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health-check', methods=['GET'])
def health_check():
    return jsonify(status="healthy"), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
