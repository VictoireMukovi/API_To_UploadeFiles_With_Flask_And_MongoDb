from flask import Flask,request,jsonify,Response
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson.binary import Binary
import os
import uuid

app=Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['dbFichier']
collection = db['images']

#Uploade directement une images dans la base des donn2es
@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    image_binary = Binary(file.read())
    collection.insert_one({'image': image_binary})
    return 'Image uploaded successfully!'

@app.route('/image/<image_id>')
def get_image(image_id):
    image_data = collection.find_one({'_id': ObjectId(image_id)})
    return Response(image_data['image'], mimetype='image/jpeg')
    #return jsonify({image_data['image'], mimetype='image/jpeg')})


if __name__=="__main__":
    app.run(debug=True)

