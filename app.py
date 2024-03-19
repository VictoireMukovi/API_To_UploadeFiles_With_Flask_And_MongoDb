from flask import Flask,request,jsonify,Response
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson.binary import Binary
import os
import uuid
from werkzeug.utils import secure_filename

# Importer la librairie MongoClient pour interagir avec MongoDB
from pymongo import MongoClient

# Créer une connexion au serveur MongoDB sur localhost et port 27017
client = MongoClient('mongodb://localhost:27017/')

# Sélectionner la base de données nommée 'dbFichier'
db = client['dbFichier']

# Sélectionner la collection nommée 'imagesInFolder' à l'intérieur de la base de données
collection = db['imagesInFolder']

# Définir un ensemble d'extensions de fichiers autorisées pour le téléchargement
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg'])

# Créer une instance de l'application Flask
app = Flask(__name__)

# Configurer le dossier de destination pour les fichiers téléchargés
app.config['UPLOAD_FOLDER'] = 'uploadsFolder'

def allowed_file(filename):
  """
  Cette fonction vérifie si l'extension d'un fichier est autorisée pour le téléchargement.

  Args:
      filename (str): Le nom du fichier à vérifier.

  Returns:
      bool: True si l'extension est autorisée, False sinon.
  """

  # Vérifier si le nom de fichier contient un point (séparateur d'extension)
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/media/upload', methods=['POST'])
def upload_media():
  """
  Cette fonction gère l'upload de fichiers via la route '/media/upload'.

  Returns:
      JSON: Une réponse JSON en fonction du résultat de l'upload.
  """

  # Vérifier si un fichier a été envoyé via le champ 'file' du formulaire
  if 'file' not in request.files:
    # Retourner une erreur 400 si aucun fichier n'est présent
    return jsonify({'error': 'Aucun média fourni'}), 400

  # Récupérer le fichier envoyé depuis le formulaire
  file = request.files['file']

  # Vérifier si le nom de fichier est vide (sélection annulée)
  if file.filename == '':
    # Retourner une erreur 400 si aucun fichier n'est sélectionné
    return jsonify({'error': 'Aucun fichier sélectionné'}), 400

  # Vérifier si le fichier est valide en fonction des extensions autorisées
  if file and allowed_file(file.filename):
    # Sécuriser le nom de fichier pour éviter les injections
    filename = secure_filename(file.filename)

    # Enregistrer le fichier dans le dossier configuré
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Préparer les données à insérer dans la base de données
    image_data = {
      'filename': file.filename,
      'path': filename
    }

    # Insérer les données du fichier dans la collection 'imagesInFolder'
    if collection.insert_one(image_data):
      # Retourner une réponse de succès (code 200) avec un message
      return jsonify({'msg': 'Photo ajoutée avec succès'}), 200

  # Si le fichier n'est pas valide, on ne rentre pas dans le bloc if précédent
  # Retourner une erreur 400 pour informer l'utilisateur
  return jsonify({'error': 'Type de fichier non autorisé'}), 400
@app.route('/get_image')
def get_images():
  """
  Cette fonction récupère toutes les images de la collection 'imagesInFolder'.

  Returns:
      list: Une liste d'objets image contenant le nom et le chemin d'accès.
  """

  # Récupérer tous les documents de la collection
  images = collection.find({})

  # Préparer une liste pour stocker les données des images
  image_list = []

  # Parcourir chaque document
  for image in images:
    # Extraire le nom et le chemin d'accès de l'image
    image_data = {
      'filename': image['filename'],
      'path': image['path']
    }

    # Ajouter les données à la liste
    image_list.append(image_data)

  # Retourner la liste d'images
  return image_list


if __name__=="__main__":
    app.run(debug=True)

