import pandas as pd
import numpy as np
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("key.json")
try:
    firebase_admin.initialize_app(cred)
except:
    pass
db = firestore.client()


class FireBase:

    user_data = {}

    def __init__(self):

        self.db = firestore.client()
        self.user_data["Drinking"] = 'NA'
        self.user_data["Smoking"] = 'NA'
        self.user_data["Gender"] = 'NA'
        # self.user_data["Name"] = 'NA'
        self.user_data["Id"] = 'NA'

    def GetD(self):
        # db = firestore.client()
        self.users_ref = db.collection(u'root')
        self.docs = self.users_ref.stream()
        for doc in self.docs:
            self.user_data["Drinking"] = u'{}'.format(
                doc.to_dict()['Drinking'])
            self.user_data["Smoking"] = u'{}'.format(doc.to_dict()['Smoking'])
            self.user_data["Gender"] = u'{}'.format(doc.to_dict()['Gender'])
            # self.user_data["Name"] = u'{}'.format(doc.to_dict()['n'])
            self.user_data["Id"] = u'{}'.format(doc.id)
        return(self.user_data)

    def SendD(self, cluster, id):
        self.users_refx = db.collection(u'root').document(
            id).collection(u'OnBdCluster')
        self.users_refx.set({u'ClusterNumber': cluster}, merge=True)
        return 'ClusterID uploaded'


def MCFunc():
    x = FireBase()
    see = x.GetD()
    # print(see)
    return see


def EAFunc(persona, id):
    x = FireBase()
    x.SendD(persona, id)
