import os
import pathlib
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__, static_folder = '.', static_url_path = '')

p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
docs_list = list(p.glob("*.docx"))
file_list = []
for doc in docs_list:
    file_list.append(str(doc).split("\\")[-1])

@app.route('/')
def index():
    return render_template("test.html", items = file_list)


# @app.route('/upload', methods=['POST'])
# def upload():
#     data = request.get_json()
#     folderPath = data.get('folderPath', [])
#     response_message = f'受信したフォルダパス: {", ".join(folderPath)}'
#     return response_message

@app.route('/post_text', methods=['POST'])
def post_text():
    text = request.json.get('text', '')

    select_words = []
    select_words.append("text")

    tmp = []
    for file in file_list:
        for word in select_words:
            if word in str(file):
                tmp.append(str(file))

    json_data = {"items": tmp}

    # ここでテキストを処理または保存することができます
    return json.dumps(json_data)


app.run(port = 8000, debug = True)