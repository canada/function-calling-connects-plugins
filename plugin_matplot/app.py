import sys
import os

# 親ディレクトリをパスに追加
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, parent_dir)

from flask import Flask, jsonify, send_from_directory, request, Blueprint

app = Flask(__name__, static_folder='static')

import io
import sys

@app.route('/python_execute', methods=['POST'])  # ルートをBlueprintに登録
def python_execute():
    data = request.get_json()

    data['code'] = "import japanize_matplotlib\nfrom mpl_toolkits.mplot3d import Axes3D\n" + data['code']
    # ログを出力
    print(data['code'])

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # 標準出力を一時的にリダイレクト
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()

    try:
        exec(data['code'])
        sys.stdout = old_stdout
        output = redirected_output.getvalue()
        return jsonify({"message": "Code executed successfully", "output": output}), 200
    except Exception as e:
        sys.stdout = old_stdout
        return jsonify({"error": str(e)}), 500

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