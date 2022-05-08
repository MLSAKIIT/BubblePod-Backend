from bin.data import db 
import numpy as np
import pandas as pd
import bin.cluster.models as models


class Cluster:
    def __init__(self, debug=False):
        self.bubbledb = db.bubbledb()
        self.dataframe = self.bubbledb.table_to_dataframe("accounts")
        self.preprocess()
        self.model = models.VecModel()
        self.debug = debug


    def preprocess(self):
        self.dataframe.drop(["index", "username", "email"], axis=1, inplace=True)
        try:
            self.dataframe.drop(["cluster"], axis=1, inplace=True)
        except:
            pass


    def vectorise(self):
        vectors = []
        interests = self.dataframe.values.tolist()
        if self.debug:
            print(interests)
        for interest in interests:
            # print(interest)
            vectors.append(self.model.infer(interest))
        return np.asarray(vectors)


    def store_clusters(self, labels):
        self.dataframe = self.bubbledb.table_to_dataframe("accounts")
        self.dataframe['cluster'] = labels
        self.bubbledb.dataframe_to_table(self.dataframe)


    def clusters(self):
        x = self.vectorise()
        labels = self.model.dbscan(x, self.debug)
        if self.debug:
            print(x)
            print(labels)
            print(self.dataframe)
        self.store_clusters(labels)

    
    def find_similar(self, label):
        output_frame = self.dataframe.loc[self.dataframe['username'] == label]
        if self.debug:
            print(output_frame.head())
        return output_frame

    def plot():
        #Needs to be implemented
        pass



def dummyvalues():
    bubbledb = db.bubbledb()
    bubbledb.create_main_table()
    import random
    data = []
    for i in range(4500):
        data1 = [f'dasykfhhh{i}89', f'2g828106{i}@gmail.com']
        data2 = ['Blockchain', 'App_Development', 'Cryptography']
        data = data1 + [random.choice(data2), random.choice(data2), random.choice(data2)]
        bubbledb.insert("accounts", data)
