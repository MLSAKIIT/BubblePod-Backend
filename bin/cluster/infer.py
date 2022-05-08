from bin.data import db 
import numpy as np
import pandas as pd
import bin.cluster.models as models


class Cluster:
    def __init__(self, bubbledb, debug=False):
        self.bubbledb = bubbledb
        self.dataframe = self.bubbledb.table_to_dataframe("accounts")
        self.dataset = self.dataframe.drop(["index", "username", "email", "clutser"], inplace=True)
        self.model = models.VecModel()
        self.debug = debug


    def dummyvalues(self):
        import random
        data = []
        for i in range(4500):
            data1 = [f'dasykfhhh{i}89', f'2g828106{i}@gmail.com']
            data2 = ['Blockchain', 'App_Development', 'Cryptography']
            data = data1 + [random.choice(data2), random.choice(data2), random.choice(data2)]
            self.bubbledb.insert(data)


    def vectorise(self):
        vectors = []
        data = self.dataset.values.tolist()
        print(data)
        for interests in data:
            for interest in interests:
                print(interest)
                vectors.append(self.model.infer(interest))
        return np.asarray(vectors)


    def clusters(self):
        x = self.vectorise()
        print(x)
        labels = self.model.dbscan(x, self.debug)
        if self.debug:
            print(labels)
        self.dataset['cluster'] = labels
        print(self.dataset)
        self.bubbledb.dataframe_to_table(self.dataset)

    
    def find_similar(self, label):
        # label = self.bubbledb.fetch(username)
        output_frame = self.dataset.loc[self.dataset['cluster'] == label]
        if self.debug:
            print(output_frame.head())
        return output_frame

    def plot():
        #Needs to be implemented
        pass


# dummyvalues(bubbledb)
# cluster = Cluster(debug=True)
# cluster.clusters()
# cluster.find_similar(2)

# bubbledb = db.bubbledb()
# def dummyvalues():
#     bubbledb = db.bubbledb()
#     bubbledb.create_main_table()
#     import random
#     data = []
#     for i in range(4500):
#         data1 = [f'dasykfhhh{i}89', f'2g828106{i}@gmail.com']
#         data2 = ['Blockchain', 'App_Development', 'Cryptography']
#         data = data1 + [random.choice(data2), random.choice(data2), random.choice(data2)]
#         bubbledb.insert("accounts", data)
# dummyvalues()


# print(dataset.head())
# engine = sqlalchemy.create_engine('postgresql://postgres:password@localhost:5432/bubblepod')
# dataset.to_sql('accounts', engine, if_exists="replace", index=False)
# data = dataset.values.tolist()
# for interest in data:
#     print(interest)

bubbledb = db.bubbledb()
cluster = Cluster(bubbledb,debug=True)
print(cluster.vectorise())
