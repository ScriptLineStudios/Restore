from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import shutil

app = Flask(__name__)

@app.route("/upload/<name>", methods=['POST','PUT'])
def print_filename(name):
    file = request.files['file']
    with open(name, "wb") as f:
        f.write(file.read())
        
    return "", 200

@app.route("/download/<file_name>")
def download(file_name):
	print("Sending File")
	return send_file(file_name)
	

if __name__ == "__main__":
    app.run(debug=True, port=6000)
