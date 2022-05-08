import pandas as pd
from bin.data import db

def store_data(content):
    data = []
    for key in content:
        data.append(content[key])
    bubbledb = db.bubbledb()
    bubbledb.insert(data)

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

# def retrieve_data(content):
#     data = content['username']
#     cluster = Cluster()
#     result = cluster.find_similar(data)
#     print(result[:10])

# dummyvalues()
from bin.cluster.infer import Cluster