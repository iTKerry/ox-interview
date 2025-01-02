from flask import Flask

app = Flask(__name__)

from app.api import health_check, add_text, find_similar

app.add_url_rule('/health-check', view_func=health_check)
app.add_url_rule('/add_text', view_func=add_text, methods=['POST'])
app.add_url_rule('/find_similar', view_func=find_similar, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
