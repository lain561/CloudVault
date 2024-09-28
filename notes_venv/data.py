from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_talisman import Talisman #this allows us to run over HTTPS
#make sure to pip install flask-talisman

from flask import flash
import logging

app = Flask(__name__)

# In-memory storage for notes (for simplicity)
notes = []

#configing a secret key
app.config['key'] = 'secretKey'

#allow us to render an index HTML5 file for user
@app.route('/')
def index():
    return render_template('index.html', notes=notes)

@app.route('/pages')
def another():
    return render_template('subFolder/upload.html')

#redirects the POST to index (I think?)
@app.route('/add', methods=['POST'])
def add_note():
    note = request.form.get('note')
    if note:
        notes.append(note)
    return redirect(url_for('index'))


#file uploading handling, we will set a limit to 16 MB for now
@app.route('/upload', methods = ['POST'])
def uploadingFile():
    if 'file' not in request.files:
        return "No file found"
    inFile = request.files['file']
    if inFile.filename == '':
        return "No File Selected"
    if inFile:
        filename = secure_filename(inFile.filename)
        inFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "File Upload Complete"

#HTTPS stuff
Talisman(app)

#we want to put some restrictions on imports of certain files types
#for now lets just work on PNG and JPG
EXTENSIONS = {'png', 'jpg'}

#function for restriction of file types
def permittedFiles(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in EXTENSIONS #just checking the file type (setting the chars to lowercase for comparing everything)

#keeping track of uploads and errors that occur
logging.basicConfig(level = logging.INFO)


if __name__ == '__main__':
    app.run(ssl_context=('certificate.pem', 'private_key.pem'), debug=True) #just debugging..not needed? Kinda just left this here
#I think we need an SSL? not sure...