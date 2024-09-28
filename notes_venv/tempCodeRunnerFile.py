#function for restriction of file types
def permittedFiles(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in EXTENSIONS #just checking the file type (setting the chars to lowercase for comparing everything)

#keeping track of uploads and errors that occur
logging.basicConfig(level = logging.INFO)

#providing feedback to users
flash('FILE UPLOAD SUCESSFULL')