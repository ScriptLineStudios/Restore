from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import io
from cryptography.fernet import Fernet
import requests
import config
import gc

app = Flask(__name__)

relays = ["http://127.0.0.1:6000", "http://192.168.68.120:6000"]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add_relay/address", methods=['POST'])
def add_relay(address):
    relays.append(address)
    return "", 200

@app.route("/upload/<name>", methods=['POST'])
def upload(name):
    file = request.files['file']    
    for index, relay in enumerate(relays):
        try:
            requests.post(f"{relay}/upload/{name}", files={"file": file})
        except:
            pass
    return jsonify(sucess="Success")

@app.route("/download/<file_name>/<key>",methods=['GET'])
def download(file_name, key):
    for relay in relays:
        try:
            r = requests.get(f"{relay}/download/{file_name}")
            f = Fernet(key)
            data = f.decrypt(r.content)
            return send_file(io.BytesIO(data), as_attachment=True, download_name=file_name)
        except:
            continue

if __name__ == "__main__":
    app.run(debug=True)
