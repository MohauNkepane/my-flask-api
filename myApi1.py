from flask import Flask,request
from flask_restful import Resource, Api
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



cred = credentials.Certificate("creative-explosion-firebase-adminsdk-3tjnu-313071f290.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

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
class users(Resource):
    def get(self):
        return {"Msg":"Users"}
class poems(Resource):

    def post(self):
        #Method for posting a single poem to Firestore

        #Get poems data as a request from front-end or postman
        data = request.json
        
        title = data["title"]
        poem_content = data["poem_content"]
        rating = data["rating"]
        no_of_reads = data["no_of_reads"]
        poet_id = data["poet_id"]
        likes = data['likes']

        genres = data["genres"]
        #fetching values from the genres object.
        ballad =genres["ballad"]
        elegy=genres["elegy"]
        #print(elegy)

        #Saving the poem on firestore.
        doc_ref = db.collection(u'poems').document(u'poem3')
        doc_ref.set({
            u'title': u'{}'.format(title),
            u'poem_content' : u'{}'.format(poem_content),
            u'rating': rating,
            u'no_of_reads': no_of_reads,
            u'poet_id': u'{}'.format(poet_id),
            u'likes': likes,
            u'genres': {
                u'elegy': elegy,
                u'ballad': ballad
            }
        })
        return {"Msg" : "Stored"}


    def get(self):
        poems_ref = db.collection(u'poems')
        docs = poems_ref.stream()


        for doc in docs:
            print(f'{doc.id} => {doc.to_dict()}')
        return {"Msg" : "retrieved"}

class books(Resource):
    def get(self):
        return Data

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'Mohau'}

# api.add_resource(HelloWorld, '/')

api.add_resource(books, '/') #endpoint for all books
api.add_resource(book, '/Name/<string:name>') #endpoint for single books.
api.add_resource(poems, '/poems')
#more endpoints looding...

if __name__ == '__main__':
    app.run(debug=True)