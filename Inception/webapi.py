# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 22:21:28 2017

@author: Frank

ref: https://stackoverflow.com/questions/10434599/how-to-get-data-received-in-flask-request
     https://www.reddit.com/r/flask/comments/5fl0xn/multifile_api_using_requests/
     https://github.com/mastercoder82/flask-test
     https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
     https://stackoverflow.com/questions/10434599/how-to-get-data-received-in-flask-request
     (request.data Contains the incoming request data as string in case it came with a mimetype Flask does not handle.)
     (request.files: the files in the body, which Flask keeps separate from form. HTML forms must use enctype=multipart/form-data or files will not be uploaded.)
     https://stackoverflow.com/questions/45484841/upload-image-via-python-script-to-python-flask-api
"""
import os
from flask import Flask, request, redirect, url_for,jsonify
from werkzeug import secure_filename
from classify import Classifier
import json
import time
#from os.path import basename

app = Flask(__name__)#, static_folder='static', static_url_path='')

UPLOAD_FOLDER = 'uploads'
app.classifier = Classifier()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024    # 1 Mb limit
#app.config['AZURE_STORAGE_ACCOUNT'] = "flasktest"
#app.config['AZURE_STORAGE_CONTAINER'] = "doc"
#app.config['AZURE_STORAGE_KEY'] = os.environ['AZURE_STORAGE_KEY']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/rupload/<filename>", methods=['POST', 'PUT'])
def rupload(filename):
    # Sanity checks and setup skipped.

    filename = secure_filename(filename)
    fileFullPath = os.path.join(UPLOAD_FOLDER, filename)

    with open(fileFullPath, 'wb') as f:
        f.write(request.get_data())
    
    thisis = app.classifier.run(fileFullPath)
    
    return jsonify({
        'result:': thisis
        })
       
if __name__ == "__main__":
    app.run()#host= '0.0.0.0', debug=True, port=4000)
