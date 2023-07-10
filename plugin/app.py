import sys
import os

# 親ディレクトリをパスに追加
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, parent_dir)

from flask import Flask, jsonify, send_from_directory
from mock_data import get_travel_products, get_region_overview, get_recommended_spots

app = Flask(__name__, static_folder='static')

@app.route('/travel_products', methods=['GET'])
def travel_products(arg):
    products = get_travel_products()
    return jsonify(products=products)

@app.route('/region_overview', methods=['GET'])
def region_overview(arg):
    region_data = get_region_overview(arg)
    print(region_data)
    return jsonify(region_data)

@app.route('/recommended_spots', methods=['GET'])
def recommended_spots(arg):
    spots = get_recommended_spots()
    return jsonify(spots=spots)

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
