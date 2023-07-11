import sys
import os

# 親ディレクトリをパスに追加
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, parent_dir)

from flask import Flask, jsonify, send_from_directory, request
from mock_data import search_restaurants, make_reservation

app = Flask(__name__, static_folder='static')

@app.route('/search_restaurants', methods=['GET'])
def search_restaurants_route():
    query = request.args.get('query')
    date = request.args.get('date')
    party_size = int(request.args.get('party_size'))

    if not all([query, date, party_size]):
        return jsonify({"error": "Missing required parameters"}), 400

    restaurants = search_restaurants(query, date, party_size)
    return jsonify(restaurants=restaurants)

@app.route('/make_reservation', methods=['POST'])
def make_reservation_route():
    restaurant_id = request.form.get('restaurant_id')
    date = request.form.get('date')
    time = request.form.get('time')
    party_size = int(request.form.get('party_size'))

    if not all([restaurant_id, date, time, party_size]):
        return jsonify({"error": "Missing required parameters"}), 400

    reservation = make_reservation(restaurant_id, date, time, party_size)
    return jsonify(reservation=reservation)

@app.route('/logo.png', methods=['GET'])
def plugin_logo():
    return send_from_directory(app.static_folder, 'logo.png')

@app.route('/.well-known/ai-plugin.json', methods=['GET'])
def plugin_manifest():
    return send_from_directory(app.static_folder, '.well-known/ai-plugin.json')

@app.route('/openapi.yaml', methods=['GET'])
def openapi_spec():
    return send_from_directory(app.static_folder, 'openapi.yaml', mimetype='text/yaml')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
