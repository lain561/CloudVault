from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask import flash
import logging

#we want to put some restrictions on imports of certain files types
EXTENSIONS = {'png', 'jpg', 'txt', 'pdf', 'doc', 'docx', 'zip', 'tar', 'rar'}

#initialize flask application and then refer the instance as app
app = Flask(__name__)

#secret key for flash
app.secret_key = 'some_key'

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
def uploadStuff():
    return render_template('subFolder/upload.html')

@app.route('/about')
def aboutStuff():
    return render_template('subFolder/about.html')

@app.route('/idx')
def index2():
    return render_template('index.html')


#file uploading handling, we will set a limit to 16 MB for now
#we'll refresh the page after upload to the user can easily upload again
@app.route('/upload', methods = ['GET', 'POST'])
def uploadingFile():
    if 'file' not in request.files:
        flash('No file found')
        return redirect(url_for('uploadStuff'))
    inFile = request.files['file']
    if inFile.filename == '':
        flash('No File Selected')
        return redirect(url_for('uploadStuff'))
    if not permittedFiles(inFile.filename): #call a function that check to see if the file is allowed to upload
        flash('File not Allowed')
        return redirect(url_for('uploadStuff'))
    if inFile:
        filename = secure_filename(inFile.filename)
        inFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #we can save this crap to the uploads folder
        flash('File uploaded successfully!')  # Flash a message
        return redirect(url_for('uploadStuff'))

#function for restriction of file types
def permittedFiles(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in EXTENSIONS #just checking the file type (setting the chars to lowercase for comparing everything)

#keeping track of uploads and errors that occur
logging.basicConfig(level = logging.INFO)


if __name__ == "__main__":
    try:
        app.run(ssl_context=('certificate.pem', 'private_key.pem'), debug=True, host='0.0.0.0', port=5500) #I created a self-certificate for HTTPS. We now have SSL implemented
    except Exception as e:
        print(f"Error: {e}") 