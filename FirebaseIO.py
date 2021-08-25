import pandas as pd
import numpy as np
import json
import firebase_admin
from firebase_admin import _FIREBASE_CONFIG_ENV_VAR, credentials
from firebase_admin import firestore
from pandas.io.pytables import GenericDataIndexableCol
cred = credentials.Certificate(r"key.json")
try:
    firebase_admin.initialize_app(cred)
except:
    pass
db = firestore.client()


class FireBase:

    user_data = {}

    def __init__(self):

        self.db = firestore.client()
        self.user_data["Drinking"] = "NA"
        self.user_data["Smoking"] = "NA"
        self.user_data["Gender"] = "NA"
        self.user_data["Id"] = "NA"
        self.user_data["Name"] = "NA"
        # self.user_data[""] = "NA"
        # self.user_data[""] = "NA"

    def TryD(self):
        # db=firestore.client()
        self.docs = self.db.collection(u'root').stream()
        x = []
        for doc in self.docs:
            y = (f'{doc.id} => {doc.to_dict()}')
            x.append(y)

    def GetD(self):
        # print('collecting from document')
        db = firestore.client()
        self.users_ref = db.collection(u'root').stream()
        # self.docs = self.users_ref.stream()
        tests = []
        print(self.users_ref)
        for doc in self.users_ref:
            self.user_data["Drinking"] = u'{}'.format(
                doc.to_dict()['Drinking'])
            self.user_data["Smoking"] = u'{}'.format(doc.to_dict()['Smoking'])
            self.user_data["Gender"] = u'{}'.format(doc.to_dict()['Gender'])
            self.user_data["Name"] = u'{}'.format(doc.to_dict()['Name'])
            self.user_data["Id"] = u'{}'.format(doc.id)
            tests.append(self.user_data)
        # for eh in tests:
        #     print(eh)
        #     print(type(eh))

    def SendD(self):
        # print('uploading data')
        # Udpdate:

        db.collection(u'root').document(
            self.user_data["Id"]).collection(u'ClusterNo').set(self.user_data)
        # doc = self.users_ref.document(item.id) # doc is DocumentReference
        # field_updates = #jsonify the dataset
        # doc.update(field_updates)

    def GetS(self):
        self.GetD()
        return(self.user_data)


def classfree(idg):
    # docs = db.collection(u'DummyMLAIHardik').stream()
    docs = db.collection(u'root').where(
        firestore.key, '==', idg).get()
    print(type(docs))
    print(docs)
    # x = []
    # df = pd.DataFrame
    # for  doc in docs:
    # x["Drinking"] = "NA"
    # x["Smoking"] = "NA"
    # x["Gender"] = "NA"
    # x["Id"] = "NA"
    # x["Name"] = "NA"
    # x = []
    # for doc in docs:
    #     y = (f'{doc.id} => {doc.to_dict()}')
    #     x.append(y)
    # print(type(x))
    # print(x)
    # it = iter(x)
    # res = dict(zip(it, it))
    # print(type(res))
    # print(res)
    # for i in range(len(x)):
    #     print(x[i])
    # print(type(x[i]))
    # xx = str(x[i])
    # y = exec(xx)
    # print(type(y))
    # y = json.loads(x)

    # df = df.join(res)

    return docs


def ModelO():

    return 'Its  uploasded  to firebase'


def MCFunc():
    x = FireBase()
    see = x.GetS()
    # print(see)
    return see
