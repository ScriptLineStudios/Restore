from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import io
from cryptography.fernet import Fernet
import requests
import config
import pickle
import hashlib

app = Flask(__name__)

pickle.dump([], open("relays.pickle", "wb"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add_relay/<address>", methods=['POST'])
def add_relay(address):
    relays = pickle.load(open("relays.pickle","rb"))
    relays.append("http://" + address)
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

@app.route("/download/<hash_encrypted>/<file_name>/<key>",methods=['GET'])
def download(hash_encrypted, file_name, key):
    relays = pickle.load(open("relays.pickle", "rb"))
    for relay in relays:
        try:
            r = requests.get(f"{relay}/download/{file_name}")
            relay_hash = hashlib.sha256(r.content).hexdigest()
            if str(relay_hash) == str(hash_encrypted):
                print("Allowing file download")
                return send_file(io.BytesIO(r.content), as_attachment=True, download_name=file_name)
            else:
                print("File has been modified relay side, skipping...")
                return "", 200
        except Exception as e:
            continue
    return "", 200

if __name__ == "__main__":
    app.run(debug=True)
