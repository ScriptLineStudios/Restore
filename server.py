from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import io
from cryptography.fernet import Fernet
import requests
import config
import gc

app = Flask(__name__)

relays = ["http://127.0.0.1:6000"]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload/<name>", methods=['POST'])
def upload(name):
    for index, relay in enumerate(relays):
        gc.collect()
        file = request.files['file']    
        requests.post(f"{relay}/upload/{name}", files={"file": file})
        return jsonify(realy=str(index))

@app.route("/download/<file_name>/<key>",methods=['GET'])
def download(file_name, key):
    r = requests.get(f"{config.BACKEND_URL}/download/{file_name}")
    f = Fernet(key)
    data = f.decrypt(r.content)
    return send_file(io.BytesIO(data), as_attachment=True, download_name=file_name)

if __name__ == "__main__":
    app.run(debug=True)
