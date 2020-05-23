import os

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename


# https://pythonise.com/series/learning-flask/flask-uploading-files

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # Max 2 megabytes file
app.config["UPLOAD_FOLDER"] = './file_storage'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def redirect_user():
    '''Redirect the user to our main page'''
    return redirect(url_for('upload_file'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    '''Get the file from the user'''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print('No file part')
            app.logger.error('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('read_user_input', filename=filename))

    return render_template('upload.html')

@app.route('/table')
def read_user_input():
    '''Get the file, convert them to list of dicts and load to db'''
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('filename'))
    # file_content = read_this_file(file_path)
    file_content = "PLIK przeczytany"
    return file_content


if __name__ == "__main__":
    app.run(debug=False)
