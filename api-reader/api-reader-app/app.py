# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from adb import retrieve_data
import json

import logging
  
# creating the flask app
app = Flask(__name__)
CORS(app)
# creating an API object
api = Api(app)
  
# making a class for a particular resource
# the get, post methods correspond to get and post requests
# they are automatically mapped by flask_restful.
# other methods include put, delete, etc.
class DataDb(Resource):
  
    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
  
        data = retrieve_data()
        return json.loads(data.encode().decode('utf-8'))
        #return jsonify(data, status=200, mimetype='application/json')
        
  
    # Corresponds to POST request
    def post(self):
    
        data = request.get_json()
        #return jsonify(data, ensure_ascii=False, status=200, mimetype='application/json')
        return jsonify({"data":data}, status=200, mimetype='application/json')
  
  
# another resource to calculate the square of a number
class Square(Resource):
  
    def get(self, num):
  
        return jsonify({'square': num**2})
  
  
# adding the defined resources along with their corresponding urls
api.add_resource(DataDb, '/')
api.add_resource(Square, '/square/<int:num>')
  
  
# driver function
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
    #app.run(debug = True)
