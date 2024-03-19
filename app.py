from flask import Flask,request,jsonify,Response
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson.binary import Binary
import os
import uuid
from werkzeug.utils import secure_filename




# Configuration de la connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['dbFichier']
collection = db['imagesInFolder']
# Répertoire pour stocker les images téléchargées
UPLOAD_FOLDER = 'uploadsFolder'
ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg'])
app=Flask(__name__)
app.config['UPLOAD_FOLDER']='uploadsFolder'

def allowed_file(fielename):
    return '.' in fielename and fielename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS

@app.route('/media/upload',methods=['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({'error':'media not provided'}),400
    file=request.files['file']
    if file.filename=='':
        return jsonify({'error':'no file selected'}),400
    if file and allowed_file(file.filename):
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    return jsonify({'msg':'Photo ajouter avec succes'}),200

'''# Répertoire pour stocker les images téléchargées
UPLOAD_FOLDER = 'uploadsFolder'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Vérifie si la requête contient un fichier
        fichier=request.files['image']
        if 'file' not in fichier:
            return 'No file part'
        file = request.files['image']
        # Si l'utilisateur n'a pas sélectionné de fichier, le navigateur envoie une chaîne vide sans nom de fichier.
        if file.filename == '':
            return 'No selected file'
        if file:
            # Enregistre le fichier téléchargé dans le répertoire d'uploads
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            # Insérer le chemin d'accès de l'image dans la base de données
            image_data = {
                'filename': file.filename,
                'path': filename
            }
            collection.insert_one(image_data)
            return 'File uploaded successfully'''

if __name__=="__main__":
    app.run(debug=True)

