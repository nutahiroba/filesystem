from flask import Flask, render_template, request, jsonify
import pathlib

app = Flask(__name__, static_folder = '.', static_url_path = '')

p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
docs_list = list(p.glob("*.docx"))
file_list = []
for doc in docs_list:
    file_list.append(str(doc).split("\\")[-1])

global select_words

@app.route('/')
def index():
    select_words = []
    return render_template("wc.html")


# @app.route('/upload', methods=['POST'])
# def upload():
#     data = request.get_json()
#     folderPath = data.get('folderPath', [])
#     response_message = f'受信したフォルダパス: {", ".join(folderPath)}'
#     return response_message


select_words = []

@app.route('/post_text', methods=['POST'])
def post_text():
    text = request.json.get('text', '')

    if text in select_words:
        select_words.remove(text)
    else:
        select_words.append(text)

    flg = 0

    tmp = []
    for file in file_list:
        if all(word in file for word in select_words):
            tmp.append(file)
    
    print(text, select_words)

    if len(tmp) == 0:
        json_data = {"items":"undified"}
    else:
        json_data = {"items": tmp}
<<<<<<< HEAD
=======

    
    print(json_data)
>>>>>>> 4e9e6956bdc80c0b106207a4b6bd3e92daabd8dc

    return jsonify(json_data)

if __name__ == '__main__':
    app.run(port = 8000, debug=True)
