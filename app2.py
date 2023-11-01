from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

recorded_text_list = []

@app.route('/')
def index():
    return render_template("wc.html")

@app.route('/sendList', methods=['POST'])
def send_list():
    data = request.get_json()
    received_text_list = data.get('recordedTexts', [])
    tmp = []
    for file in received_text_list:
        if all(word in file for word in received_text_list):
            tmp.append(file)

    if len(tmp) == 0:
        json_data = {"items":"undified"}
    else:
        json_data = {"items": tmp}

    return jsonify(json_data)

if __name__ == '__main__':
    app.run(port = 8000, debug=True)
