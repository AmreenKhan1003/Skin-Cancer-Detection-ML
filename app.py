from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import pandas as pd

app = Flask(__name__)

dic = {0:'Actinic Keratoses and intraepithelial carcinoma (akiec)', 1:'Basal Cell Carcinoma (bcc)', 2:'Benign lesions of the keratosis (bkl)', 3:'Dermatofibroma (df)', 4:'Melanoma (mel)',5: 'non-cancerous image',6:'Melanocytic nevi(nv)',7:'Random image', 8:'Vascular lessions'}
prec = {0:'Actinic Keratoses and intraepithelial carcinoma (akiec)', 1:'Basal Cell Carcinoma (bcc)', 2:'Benign lesions of the keratosis (bkl)', 3:'Dermatofibroma (df)', 4:'Melanoma (mel)',5: 'non-cancerous image',6:'Melanocytic nevi(nv)',7:'Random image', 8:'Vascular lessions'}
model = load_model('model_94_9.h5')

model.make_predict_function()

def predict_label(img_path):
	i = image.load_img(img_path, target_size=(32,32))
	i = image.img_to_array(i)/255.0
	i = i.reshape(1, 32,32,3)
	p =  np.argmax(model.predict(i),axis=1)
	return dic[p[0]], prec[p[0]]

@app.route('/')
def home():
    return render_template('navfoot.html')

@app.route("/predicts", methods=['GET', 'POST'])
def pred():
	return render_template("predictcancer.html")

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']
		img_path = "static/" + img.filename	
		img.save(img_path)
		p,pr = predict_label(img_path)

	return render_template("predictcancer.html", prediction = p, precaution = pr, img_path = img_path)

@app.route('/types')
def types():
	return render_template('typeskin.html')

@app.route('/dermatologist')
def nearby():
	return render_template('dermatologist.html')

@app.route("/submitcity", methods=['GET', 'POST'])
def city_output():
    if request.method == 'POST':
        c= request.form['city']
        doc_data = 'doctors_data.xlsx'
        df = pd.read_excel(doc_data)
        print(df)
        r = df[['Details']].where(df['City']==c).dropna()
        print(c)
        #print(r['Name'])

    return render_template("dermatologist.html", names=r['Details'])

@app.route('/Services')
def services():
	return render_template('services.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)