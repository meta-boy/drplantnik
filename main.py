from flask import Flask, render_template, request, redirect, url_for
import os
from predict import classes

from werkzeug import secure_filename
UPLOAD_FOLDER = "D:/Workspace/Python/django/flask_hackathon/static"


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return render_template("index.html", name = "Anurag")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('diagnosed', filename=filename))

@app.route('/diagnosed/<filename>')
def diagnosed(filename):
   return render_template("diagnosed.html", name=filename, filename=filename, list= classes)

if __name__ == '__main__':
    app.run(debug=True)