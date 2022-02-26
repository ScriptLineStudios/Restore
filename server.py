from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import io
from cryptography.fernet import Fernet
import requests
import config

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['file']    
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(file.read())
    requests.post(f"{config.BACKEND_URL}/upload/{file.filename}", files={"file": encrypted})
    return jsonify(download_url=f"127.0.0.1:5000/download/{file.filename}/{str(key.decode())}")

@app.route("/download/<file_name>/<key>",methods=['GET'])
def download(file_name, key):
    r = requests.get(f"{config.BACKEND_URL}/download/{file_name}")
    f = Fernet(key)
    data = f.decrypt(r.content)
    return send_file(io.BytesIO(data), as_attachment=True, download_name=file_name)

if __name__ == "__main__":
    app.run(debug=True)
