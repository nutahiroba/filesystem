from flask import Flask, render_template, request, jsonify
import pathlib
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder = '.', static_url_path = '')

p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
docs_list = list(p.glob("*.docx"))

file_list = []

for doc in docs_list:
    file_list.append(str(doc).split("\\")[-1])

recorded_text_list = []

@app.route('/')
def index():
    return render_template("wc.html")

# @app.route('/sendpath', method = ["POST"]:)
# def send_Path():
#     data = request.get_json()
#     file_path = data.get('folderPaths', [])
#     print(file_path)

@app.route('/sendList', methods=['POST'])
def send_list():
    data = request.get_json()
    received_text_list = data.get('recordedTexts', [])
    tmp = []
    for file in file_list:
        if all(word in file for word in received_text_list):
            tmp.append(file)

    if len(tmp) == 0:
        json_data = {"items":"undified"}
    else:
        json_data = {"items": tmp}

    return jsonify(json_data)

if __name__ == '__main__':
    app.run(port = 8000, debug=True)
