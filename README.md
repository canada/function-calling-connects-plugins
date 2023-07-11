# function-calling-connects-plugins
Function callingから、ChatGPT Pluginsの実装を動的に読み取り実行する

## 準備

`.env`ファイルに以下の内容を入れ、保存する。

```bash
OPENAI_API_KEY='sk-*******************'
```

### 環境構築する

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

## 実行

`python app.py`で実行する。
