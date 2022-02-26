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

@app.route("/upload/<name>", methods=['POST'])
def upload(name):
    file = request.files['file']    
    requests.post(f"{config.BACKEND_URL}/upload/{name}", files={"file": file})
    return jsonify(sucess="Sucess!")

@app.route("/download/<file_name>/<key>",methods=['GET'])
def download(file_name, key):
    r = requests.get(f"{config.BACKEND_URL}/download/{file_name}")
    f = Fernet(key)
    data = f.decrypt(r.content)
    return send_file(io.BytesIO(data), as_attachment=True, download_name=file_name)

if __name__ == "__main__":
    app.run(debug=True)
