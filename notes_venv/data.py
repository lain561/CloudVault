from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
#from flask_talisman import Talisman 
#make sure to pip install flask-talisman

from flask import flash
import logging

#we want to put some restrictions on imports of certain files types
#for now lets just work on PNG and JPG
EXTENSIONS = {'png', 'jpg', 'txt'}

#initialize flask application and then refer the instance as app
app = Flask(__name__) 

UPLOAD_FOLDER = 'uploads' #creates the directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #configer an upload folder for where we can store the uploads sent from the HTML file upload

#if the folder does not exist create one
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#allow us to render an index HTML5 file for user
@app.route('/')
def index():
    return render_template('index.html')

#routing for our sub-pages on the website
@app.route('/uploading')
def another():
    return render_template('subFolder/upload.html')

@app.route('/about')
def another2():
    return render_template('subFolder/about.html')

@app.route('/idx')
def index2():
    return render_template('index.html')


#file uploading handling, we will set a limit to 16 MB for now
@app.route('/upload', methods = ['POST'])
def uploadingFile():
    if 'file' not in request.files:
        return "No file found"
    inFile = request.files['file']
    if inFile.filename == '':
        return "No File Selected"
    if not permittedFiles(inFile.filename): #call a function that check to see if the file is allowed to upload
        return "File not Allowed"
    if inFile:
        filename = secure_filename(inFile.filename)
        inFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #we can save this crap to the uploads folder
        return "File Upload Completed"

#function for restriction of file types
def permittedFiles(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in EXTENSIONS #just checking the file type (setting the chars to lowercase for comparing everything)

#keeping track of uploads and errors that occur
logging.basicConfig(level = logging.INFO)


if __name__ == "__main__":
    try:
        app.run(ssl_context=('certificate.pem', 'private_key.pem'), debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error starting server: {e}") #I created a self-certificate for HTTPS. We now save SSL implemented