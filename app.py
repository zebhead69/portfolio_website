from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Flask app!"

@app.route('/crypto', methods=['GET'])
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum,dogecoin',
        'vs_currencies': 'usd'
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Flask App!"

if __name__ == '__main__':
    app.run(debug=True) 
