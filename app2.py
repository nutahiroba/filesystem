from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

recorded_text_list = []

@app.route('/')
def index():
    return render_template("test2.html")

@app.route('/sendList', methods=['POST'])
def send_list():
    global recorded_text_list
    data = request.get_json()
    received_text_list = data.get('recordedTexts', [])

    # サーバーでリストを処理することができます
    # この例では、受け取ったリストをそのまま返します
    recorded_text_list = received_text_list
    response_message = {"message": "リストを受け取りました"}
    return jsonify(response_message)

if __name__ == '__main__':
    app.run(debug=True)
