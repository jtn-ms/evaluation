# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 22:21:28 2017

@author: Frank

ref: https://stackoverflow.com/questions/10434599/how-to-get-data-received-in-flask-request
     https://www.reddit.com/r/flask/comments/5fl0xn/multifile_api_using_requests/
     https://github.com/mastercoder82/flask-test
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
'''           
@app.route('/')
def root():
    return app.send_static_file('index.html')
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':        
        start_time = time.time()
        file = request.files['file']
        

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            thisis = app.classifier.run(file_path)
            os.rename(file_path, os.path.join(app.config['UPLOAD_FOLDER'], thisis + '__' + filename))


            print("--- %s seconds ---" % str (time.time() - start_time))
            return redirect("/")
            return redirect(url_for('uploaded_file',
                                    filename="facedetect-"+filename))

    from os import listdir
    from os.path import isfile, join
    htmlpic=""
    for f in listdir(UPLOAD_FOLDER):
        if isfile(join(UPLOAD_FOLDER,f)) and f != '.gitignore':
            print(f)
            htmlpic += """<span>""" + f.split('__')[0] + """--></span>""" + """
                <img width=200px height=150px src='uploads/"""+f+"""'>&nbsp;  &nbsp;
                """
    return '''
    <!doctype html>
    <head>
    <title>Vehicle Insurance</title>
    </head>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''+htmlpic

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
'''
@app.route("/rupload/<filename>", methods=['POST', 'PUT'])
def rupload(filename):
    # Sanity checks and setup skipped.

    filename = secure_filename(filename)
    fileFullPath = os.path.join(UPLOAD_FOLDER, filename)

    with open(fileFullPath, 'wb') as f:
        f.write(request.get_data())

    return jsonify({
        'filename': filename,
        'size': os.path.getsize(fileFullPath)
        })
'''    
from werkzeug import SharedDataMiddleware
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})
    
if __name__ == "__main__":
    app.run()#host= '0.0.0.0', debug=True, port=4000)
