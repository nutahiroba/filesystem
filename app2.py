from flask import Flask, render_template, request, jsonify
import pathlib
from flask_sqlalchemy import SQLAlchemy
from wc import main


class Parameter:
    def __init__(self, color, width, height, min):
        self.color = color
        self.width = width
        self.height = height
        self.min = min


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
    para = Parameter(color="jet", width=600, height=600, min=15)
    path = "C:\\Users\\nutta\\OneDrive\\ドキュメント\\授業資料"
    main.makeDB(path)
    wc = main.makeWC(para)
    return render_template("wc.html", data=wc)
    # return render_template("gen_wc.html")


@app.route("/generate", methods=["POST"])
def generate():
    color = request.form.get("color")
    height = request.form.get("height")
    width = request.form.get("width")
    min = request.form.get("min")
    # color, width, height, min
    para = Parameter(
        color=color,
        width=int(width),
        height=int(height),
        min=int(min),
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
    result_files = main.check(received_words)
    return jsonify({"items": result_files})


if __name__ == "__main__":
    app.run(port=8000, debug=True)
