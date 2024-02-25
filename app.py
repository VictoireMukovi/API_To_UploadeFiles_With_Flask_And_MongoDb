from flask import Flask,request,jsonify
from bson.objectid import ObjectId
app=Flask(__name__)





if __name__=="__main__":
    app.run(debug=True)

