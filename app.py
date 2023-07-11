import openai
from dotenv import load_dotenv
import os
import logging
import json
import importlib
from openapi_to_function_converter import OpenApiToFunctionConverter
from flask import Flask, request, render_template, jsonify

# プラグインのモジュール名を指定
MODULE_NAME = "plugin.app"
OPENAI_MODEL = 'gpt-3.5-turbo-0613'

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# 関数定義を取得
functions = OpenApiToFunctionConverter("plugin/static/openapi.yaml").get()
# プラグインの読み込み
plugin_module = importlib.import_module(MODULE_NAME)


def init_messages():
    system = """
    You are a helpful restaurant search assistant AI.
    Answer in Japanese and be polite in every message.
    Repeat the user's question and answer it.
    You can provide users with restaurant search and reservation information.
    Before call the restaurant search API, you need to ask the user for the date, time, and number of people.

    When providing restaurant search results, you tell the user the restaurants can be reserved on this chat.
    """

    return [{"role": "system", "content": system}]

messages = init_messages()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '')

    if question is None or question == '':
        return jsonify({"answer": "質問を入力してください。"})

    answer = get_answer(question, functions, plugin_module)
    answer = answer.replace("\n", "<br>")
    app.logger.info(answer)
    return jsonify({"answer": answer})

# APIキーの設定
def set_api_key():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

# JSONの16進数表現を日本語の文字列に変換するデバッグ用関数
def prettify_json(message_json):
    return json.dumps(message_json, ensure_ascii=False, indent=4)

# 質問からAIの返答を取得する
def get_answer(query, functions, plugin_module):
    global messages

    # システムプロンプト
    if query  == 'クリア':
        messages = init_messages()
        return 'クリアしました'

    # ユーザープロンプトを追加
    messages.append({"role": "user", "content": query})

    # AIの返答にFunction callがある限り繰り返す
    while True:
        # AIへ問い合わせ
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            # 会話の履歴を与える
            messages=messages,
            # 関数の定義も毎回与える
            functions=functions,
            function_call="auto",
            temperature=0.0,
        )

        # AIの返答を取得
        message = response.choices[0]["message"]
        print("AI response: ")
        print(prettify_json(message))
        print()
        
        # 関数の呼び出しが必要なければループから抜ける
        if not message.get('function_call'):
            break

        # 会話履歴に追加する
        messages.append(message)

        f_call = message["function_call"]

        # 関数の呼び出し、レスポンスの取得
        print("Function call: " + f_call["name"] + "()\nParams: " + f_call["arguments"] + "\n")

        # Flaskのappコンテキストの中の関数を無理やり呼び出す
        from flask import Flask
        app = Flask(__name__)
        with app.app_context():
            function_response = getattr(plugin_module, f_call["name"])(f_call["arguments"])

        function_response = json.dumps(function_response)
        print("Function response: " + function_response + "\n")

        # messagesに関数のレスポンスを追加
        messages.append({
            "role": "function",
            "name": f_call["name"],
            "content": function_response,
        })

    # これ以上Functionを呼び出す必要がなくなった
    print("Chain finished!")
    print()
    print("Result:")
    print(message["content"])
    return message["content"]




def cli():
    # APIキーの設定
    set_api_key()
    # 関数定義を取得
    functions = OpenApiToFunctionConverter("plugin/static/openapi.yaml").get()
    # プラグインの読み込み
    plugin_module = importlib.import_module(MODULE_NAME)

    while True:
        question = input(">> ")
        # AIの返答を取得
        answer = get_answer(question, functions, plugin_module)
        print(answer)

# APIキーの設定
set_api_key()

if __name__ == "__main__":
    app.run(debug=True)
