from flask import Flask, render_template, request, jsonify
import pathlib
from flask_sqlalchemy import SQLAlchemy
from wc import main, tfidf


class Parameter:
    def __init__(self, color, width, height, min, max, step):
        self.color = color
        self.width = width
        self.height = height
        self.min = min
        self.max = max
        self.step = step


app = Flask(__name__, static_folder=".", static_url_path="")
app.config["SQLALCHEMY_ECHO"] = False

# p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
# dfdict = main.makeDB(p)

# docs_list = p.glob("*.docx")
# file_list = []

# for doc in docs_list:
#     file_list.append(str(doc).split("\\")[-1])

# recorded_text_list = []


@app.route("/")
def index():
    # para = Parameter(color="jet", width=600, height=600, min=15)
    path = "C:\\Users\\nutta\\OneDrive\\ドキュメント\\授業資料"
    main.makeDB(path)
    tfidf.calc_tfidf()
    # wc = main.makeWC(para)
    # return render_template("wc.html", data=wc)

    return render_template("gen_wc.html")


@app.route("/generate", methods=["POST"])
def generate():
    color = request.form.get("color")
    height = request.form.get("height")
    width = request.form.get("width")
    min = request.form.get("min")
    max = request.form.get("max")
    step = request.form.get("step")
    # color, width, height, min
    para = Parameter(
        color=color,
        width=int(width),
        height=int(height),
        min=int(min),
        max=int(max),
        step=int(step),
    )
    
    wc = main.makeWC(para)

    return jsonify({"items": wc})


# @app.route('/sendpath', method = ["POST"]:)
# def send_Path():
#     data = request.get_json()
#     file_path = data.get('folderPaths', [])
#     print(file_path)


@app.route("/sendList", methods=["POST"])
def send_list():
    data = request.get_json()
    received_words = data.get("recordedTexts", [])
    match_files = main.check(received_words)
    result_files = main.getfiles(received_words, match_files)
    print(result_files)
    return jsonify({"items": result_files})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
