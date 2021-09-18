import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from google.cloud import storage
from NewModelIO import PredCluster
import pandas as pd
import jsonpickle

app = Flask(__name__)

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()


@app.route('/add', methods=['POST'])
def create():
    try:
        BUCKET_NAME = 'testmodelrepo'
        PROJECT_ID = 'testingprojects-b6504'

        # BUCKET_NAME = 'testx_model_repo'
        # PROJECT_ID = 'appsyntests-322514'
        GCS_MODEL = 'API_mini_model.joblib'

        client = storage.Client(PROJECT_ID)
        bucket = client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(GCS_MODEL)

        folder = '/tmp/'
        if not os.path.exists(folder):
            os.makedirs(folder)

        blob.download_to_filename(folder + "API_mini_model.joblib")
        id = request.json['id']
        smoking = request.json['Smoking']
        drinking = request.json['Drinking']
        gender = request.json['Gender']
        name = request.json['Name']
        all_users = db.collection('root')
        # .where('Gender', '!=', gender)
        all_users = [doc.to_dict() for doc in all_users.stream()]

        df = pd.DataFrame.from_dict(all_users)
        # df = df.drop('Name')
        df.set_index("Name", inplace=True)
        out = PredCluster(df, name)

        out = out.to_json()

        # User 1 - Smoking , Non-Drinking , Female
        # 100 Users => --U need to get me Top 50 Users that match her interests
        # I'll get the users in list and i'll upload their data in recomm users

        return str(out), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/list', methods=['POST'])
def list():
    try:
        id = request.json['Id']
        gender = request.json['Gender']
        all_users = db.collection('root').where(
            'Gender', '!=', gender).stream()
        user_list = []
        #docs = db.collection(u'cities').where(u'capital', u'==', True).stream()
        # all_users = [doc.to_dict() for doc in all_users.stream()]
        for doc in all_users:
            #print(f'{doc.id} => {doc.to_dict()}')
            d = doc.to_dict()
            user_list.append(
                users(doc.id, d['Name'], d['Gender'], d['Smoking'], d['Drinking']))

        upload_recomm_users = db.collection('root').document(
            id).collection('DateRecommended')

        #user_list2 = jsonpickle.encode(user_list, unpicklable=False)
        for index, dc in enumerate(user_list):
            print("index " + str(index) + ": " + str(dc.Id))
            data = {
                u'n': dc.Name,
                u's': dc.Smoking,
                u'd': dc.Drinking,
                u'g': dc.Gender,
                u'o': index
            }
            upload_recomm_users.document(dc.Id).set(data)
        return jsonpickle.encode(user_list, unpicklable=False), 200
    except Exception as e:
        return f"An Error Occured: {e}"


class users:
    def __init__(self, Id, Name, Gender, Smoking, Drinking):
        self.Id = Id
        self.Name = Name
        self.Gender = Gender
        self.Smoking = Smoking
        self.Drinking = Drinking


@app.route('/')
def hello():
    return 'Hello Hardik!'


if __name__ == '__main__':
    app.run(threaded=True, host='127.0.0.1', port=8080, debug=True)


# Python3 code here creating class


# # creating list
# list = []

# # appending instances to list
# list.append(users(1, 'User 1', 'Male', 'Smoking', 'Drinking'))
# list.append(users(2, 'User 2', 'Female', 'Non-Smoking', 'Non-Drinking'))
# list.append(users(3, 'User 3', 'Male', 'Non-Smoking', 'Non-Drinking'))

# for obj in list:
#     print(obj.id, obj.name, sep=' ')


# @app.route('/list', methods=['GET'])
# def reader():

#     try:
#         data = MCFunc()
#         # filterData = data["Drinking", "Smoking", "Gender"]
#         drink = data["Drinking"]
#         smoke = data["Smoking"]
#         gen = data["Gender"]
#         uid = data["Id"]
#         return drink, smoke, gen, uid

#         # personalty = mbtiPred(collected["mbti"])
#         # uid = collected["Id"]
#         # EAFunc(personalty, uid)
#         # Check if ID was passed to URL query
#         # todo_id = request.args.get('id')
#         # if todo_id:
#         #     todo = todo_ref.document(todo_id).get()
#         #     return jsonify(todo.to_dict()), 200
#         # else:
#         #     all_todos = [doc.to_dict() for doc in todo_ref.stream()]
#         #     return jsonify(all_todos), 200
#         # return str(type(all_todos))
#     except Exception as e:
#         return str(e)

# @app.route('/list', methods=['GET'])
# def read():
#     """
#         read() : Fetches documents from Firestore collection as JSON.
#         todo : Return document that matches query ID.
#         all_todos : Return all documents.
#     """
#     try:
#         # Check if ID was passed to URL query
#         todo_id = request.args.get('id')
#         if todo_id:
#             todo = todo_ref.document(todo_id).get()
#             return jsonify(todo.to_dict()), 200
#         else:
#             all_todos = [doc.to_dict() for doc in todo_ref.stream()]
#             return jsonify(all_todos), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"


# @app.route('/update', methods=['POST', 'PUT'])
# def update():
#     """
#         update() : Update document in Firestore collection with request body.
#         Ensure you pass a custom ID as part of json body in post request,
#         e.g. json={'id': '1', 'title': 'Write a blog post today'}
#     """
#     try:
#         id = request.json['id']
#         todo_ref.document(id).update(request.json)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"


# @app.route('/delete', methods=['GET', 'DELETE'])
# def delete():
#     """
#         delete() : Delete a document from Firestore collection.
#     """
#     try:
#         # Check for ID in URL query
#         todo_id = request.args.get('id')
#         todo_ref.document(todo_id).delete()
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"


# port = int(os.environ.get('PORT', 8080))
