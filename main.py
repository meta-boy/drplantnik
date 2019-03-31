from flask import Flask, render_template, request, redirect, url_for
import os


from werkzeug.utils import secure_filename
from keras import backend as K
from keras.models import load_model
from keras.preprocessing import image
from keras import optimizers
import numpy as np
import cv2


# predicting images

def classes(filename):
    # dimensions of our images
    
    img_width, img_height = 256, 256

    # load the model we saved
    model = load_model('model_1D.h5')
    model.load_weights("modelw_1D.h5")
    sgd = optimizers.SGD(lr=0.25, momentum=0.6, decay=0.0, nesterov=False)

    model.compile(loss='mean_squared_error',
                optimizer=sgd,
                metrics=['accuracy'])

    img = cv2.imread(f"static/{filename}")

    img = cv2.resize(img, (img_width, img_height))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    classes = model.predict_classes(images, batch_size=10)
    print(classes)


# print the classes, the images belong to

    

    disease_dict = {
        '0': 'Venturia inaequalis',
        '1': 'Botryosphaeria obtusa',
        '2': 'Gymnosporangium juniperi-virginianae ',
        '3': 'healthy',
        '4': 'healthy',
        '5': 'healthy',
        '6': 'Podoshaera clandestine',
        '7': 'Cercospora zeae-maydis',
        '8': 'Puccinia sorghi',
        '9': 'healthy',
        '10': 'Exserohilum turcicum',
        '11': 'Guignardia bidwellii',
        '12': 'Phaeomoniella aleophilum, Phaeomoniella chlamydospora',
        '13': 'healthy',
        '14': 'Pseudocercospora vitis ',
        '15': 'Candidatus Liberibacter spp',
        '16': 'Xanthomonas campestris',
        '17': 'healthy',
        '18': ' Xanthomonas campestris',
        '19': 'healthy',
        '20': 'Alternaria solani',
        '21': 'healthy',
        '22': 'Phytophthora infestans',
        '23': 'healthy',
        '24': 'healthy',
        '25': 'Erysiphe cichoracearum',
        '26': 'healthy',
        '27': 'Diplocarpon earlianum',
        '28': 'Xanthomonas campestris pv. vesicatoria',
        '29': 'Alternaria solani',
        '30': 'Phytophthora infestans',
        '31': 'Passalora fulva',
        '32': 'Septoria lycopersici',
        '33': 'Tetranychus urticae',
        '34': 'Corynespora cassiicola',
        '35': 'Mosaic Virus',
        '36': 'Yellow Leaf Curl Virus',
        '37': 'healthy'
    }

    K.clear_session()

    return disease_dict[str(classes[0])]



UPLOAD_FOLDER = "static"

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'JPG', 'JPEG'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('diagnosed', filename=filename))

from scrapper import Google
import asyncio
saa = ""


@app.route('/diagnosed/<filename>')
def diagnosed(filename):
    disease = classes(filename)
    medication = Google().g(disease + " medication")
    print(medication)
    
    return render_template("diagnosed.html", name=disease , filename=filename, list= medication)


if __name__ == '__main__':
    app.run(debug=True)