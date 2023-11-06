from flask import Flask, render_template, request, jsonify
import pathlib
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder = '.', static_url_path = '')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.words'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
docs_list = list(p.glob("*.docx"))

file_list = []

for doc in docs_list:
    file_list.append(str(doc).split("\\")[-1])

recorded_text_list = []

class Words(db.Model):
    file_id = db.column(db.integer, primary_key = True)
    cutwords = db.column(db.String(10000), nullable = False)

@app.route('/')
def index():
    return render_template("wc.html")

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
