from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import requests

app = Flask(__name__)
sent_request = False

@app.route("/upload/<name>", methods=['POST'])
def print_filename(name):
    file = request.files['file']
    bytes = file.read()
    with open(name, "wb") as f:
        print(bytes)
        f.write(bytes)
        
    return "", 200

@app.route("/download/<file_name>")
def download(file_name):
	print("Sending File")
	return send_file(file_name)

if not sent_request:
    address = "127.0.0.1:6000"
    data = requests.post(f"http://127.0.0.1:5000/add_relay/{address}")
    print(data)
    print("Request Made")
    sent_request = True

if __name__ == "__main__":
    app.run(debug=True, port=6000, use_reloader=False)
