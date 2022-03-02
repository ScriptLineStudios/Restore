from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import io
from cryptography.fernet import Fernet
import requests
import config
import pickle

app = Flask(__name__)

pickle.dump([], open("relays.pickle", "wb"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add_relay/<address>", methods=['POST'])
def add_relay(address):
    relays = pickle.load(open("relays.pickle","rb"))
    relays.append("http://" + address)
    print(relays)
    pickle.dump(relays, open("relays.pickle", "wb"))
    return "", 200

@app.route("/upload/<name>", methods=['POST'])
def upload(name):
    file = request.files['file']    
    relays = pickle.load(open("relays.pickle", "rb"))
    print(relays)
    for index, relay in enumerate(relays):
        try:
            requests.post(f"{relay}/upload/{name}", files={"file": file})
        except Exception as e:
            print(e)
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
