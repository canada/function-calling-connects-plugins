import openai
from dotenv import load_dotenv
import os
import logging
import json
import importlib
from openapi_to_function_converter import OpenApiToFunctionConverter
from flask import Flask, request, render_template, jsonify
from plugin_matplot import app as plugin_app

# プラグインのモジュール名を指定
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_base = os.getenv("OPENAI_API_BASE")
OPENAI_MODEL = os.getenv("OPENAI_DEPLOY_NAME_40")
MODULE_NAME = "plugin_matplot.app"

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# 関数定義を取得
# TODO  パスが環境依存している
functions = OpenApiToFunctionConverter("plugin_matplot/static/openapi.yaml").get()
print("Functions:{}\n".format(functions))

def init_messages():
    system = """
    You are a code writer and a math expert. You have access to an API that can execute code.
You use this API when you need to calculate or statistically analyze something.
Listen to the user's requirements for what they want to execute, and once you have enough information to execute the code, call the API to execute it.
You can request the API to execute source code using Matplotlib or NumPy.
You can also write plt.show().
If the user requests a result that can be plotted, try to provide the API with code that includes plt.show() as much as possible.

The plot must be complex, beautiful, and user-friendly.
You should adjust the colors in the curve as much as possible, for example, based on its speed or the elapsed time.

Use Japanese for the plot title and axis labels if you can.

If you have a result in text format, just print it as below:
print(result[:10])
The text to be printed must be small enough to use AI's context.

You use:

> fig = plt.figure()
> axes1 = fig.add_subplot(projection = '3d')

instead of:

> fig = plt.figure()
> axes1 = fig.gca(projection = '3d') 

You answer only in Japanese, not in code or markdown.

You can open the file KEN_ALL.CSV like:
open('KEN_ALL.CSV', encoding='utf-8')

The wake up word for this file is 'KEN_ALL'.

This file is as below:
この郵便番号データファイルでは、以下の順に配列しています。
- 全国地方公共団体コード（JIS X0401、X0402）………　半角数字
- （旧）郵便番号（5桁）………………………………………　半角数字
- 郵便番号（7桁）………………………………………　半角数字
- 都道府県名　…………　半角カタカナ（コード順に掲載）　（注1）
- 市区町村名　…………　半角カタカナ（コード順に掲載）　（注1）
- 町域名　………………　半角カタカナ（五十音順に掲載）　（注1）
- 都道府県名　…………　漢字（コード順に掲載）　（注1,2）
- 市区町村名　…………　漢字（コード順に掲載）　（注1,2）
- 町域名　………………　漢字（五十音順に掲載）　（注1,2）
- 一町域が二以上の郵便番号で表される場合の表示　（注3）　（「1」は該当、「0」は該当せず）
- 小字毎に番地が起番されている町域の表示　（注4）　（「1」は該当、「0」は該当せず）
- 丁目を有する町域の場合の表示　（「1」は該当、「0」は該当せず）
- 一つの郵便番号で二以上の町域を表す場合の表示　（注5）　（「1」は該当、「0」は該当せず）
- 更新の表示（注6）（「0」は変更なし、「1」は変更あり、「2」廃止（廃止データのみ使用））
- 変更理由　（「0」は変更なし、「1」市政・区政・町政・分区・政令指定都市施行、「2」住居表示の実施、「3」区画整理、「4」郵便区調整等、「5」訂正、「6」廃止（廃止データのみ使用））
※1
文字コードはUTF-8です
※2
文字セットとして、JIS X0208-1983を使用し、規定されていない文字はひらがなで表記しています。
※3
「一町域が二以上の郵便番号で表される場合の表示」とは、町域のみでは郵便番号が特定できず、丁目、番地、小字などにより番号が異なる町域のことです。
※4
「小字毎に番地が起番されている町域の表示」とは、郵便番号を設定した町域（大字）が複数の小字を有しており、各小字毎に番地が起番されているため、町域（郵便番号）と番地だけでは住所が特定できない町域のことです。

Example:
01101,"060  ","0600000","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｲｶﾆｹｲｻｲｶﾞﾅｲﾊﾞｱｲ","北海道","札幌市中央区","以下に掲載がない場合",0,0,0,0,0,0
01101,"064  ","0640941","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｱｻﾋｶﾞｵｶ","北海道","札幌市中央区","旭ケ丘",0,0,1,0,0,0
01101,"060  ","0600041","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｵｵﾄﾞｵﾘﾋｶﾞｼ","北海道","札幌市中央区","大通東",0,0,1,0,0,0
01101,"060  ","0600042","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｵｵﾄﾞｵﾘﾆｼ(1-19ﾁｮｳﾒ)","北海道","札幌市中央区","大通西（１〜１９丁目）",1,0,1,0,0,0
01101,"064  ","0640820","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｵｵﾄﾞｵﾘﾆｼ(20-28ﾁｮｳﾒ)","北海道","札幌市中央区","大通西（２０〜２８丁目）
",1,0,1,0,0,0
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

    # ログを出力
    app.logger.info("Question: " + question)

    answer = get_answer(question, functions)
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
def get_answer(query, functions):
    global messages

    # システムプロンプト
    if query  == 'クリア':
        messages = init_messages()
        return 'クリアしました'

    # ユーザープロンプトを追加
    messages.append({"role": "user", "content": query})

    # AIの返答にFunction callがある限り繰り返す
    count = 0
    while True:
        count += 1
        if count > 5:
            break

        # AIへ問い合わせ
        response = openai.ChatCompletion.create(
            engine=OPENAI_MODEL,
            # 会話の履歴を与える
            messages=messages,
            # 関数の定義も毎回与える
            functions=functions,
            function_call="auto",
            max_tokens=1000,
            temperature=0.0,
        )

        # AIの返答を取得
        message = response["choices"][0]["message"]
        print("AI response: ")
        print(prettify_json(message))
        print()
        
        # 関数の呼び出しが必要なければループから抜ける
        if not message.get('function_call'):
            break

        # APIバグ対応
        message["content"] = "."
        # 会話履歴に追加する
        messages.append(message)

        f_call = message["function_call"]

        # 関数の呼び出し、レスポンスの取得
        print("Function call: " + f_call["name"] + "()\nParams: " + f_call["arguments"] + "\n")

        # POSTの場合
        with plugin_app.app.test_client() as c:
            data = f_call["arguments"]
            print('/' + f_call["name"])
            function_response = c.post('/' + f_call["name"], data=data, content_type='application/json').get_json()

        # GETの場合
        #with app.app_context():
        #    function_response = getattr(plugin_module, f_call["name"])(f_call["arguments"])

        print(function_response)
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
