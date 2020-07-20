from flask import Flask,request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


Data = [] # soon to replaced with a firestore db

# This class will handle single books
class book(Resource):
    def get(self,name):
        for x in range(len(Data)):
            if Data[x]['Data'] == name:
                return Data[x]
        return 'Not Found', 404
    def post(self,name):
        temp = {'Data' : name}
        Data.append(temp)
        return temp

    def delete(self,name):
        for x in range(len(Data)):
            if Data[x]['Data'] == name:
                Data.pop(x)
                return "Successfully Deleted", 200
        return "No Such Item", 201

#This class will handle our whole collection of books
class books(Resource):
    def get(self):
        return Data

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'Mohau'}

# api.add_resource(HelloWorld, '/')

api.add_resource(books, '/') #endpoint for all books
api.add_resource(book, '/Name/<string:name>') #endpoint for single books.
#more endpoints looding...

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')