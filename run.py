from bin.data import db


def store_user(content):
    bubbledb = db.bubbledb()
    try:
        bubbledb.create_main_table()
    except:
        pass
    data = []
    #ensure correct arrangement of data
    keys = ['username', 'name', 'email', 'interest1', 'interest2', 'interest3']
    for key in keys:
        data.append(content[key])
    bubbledb.insert("accounts", data)


def retrieve_user(content):
    bubbledb = db.bubbledb()
    username = content.get("username")
    data = bubbledb.fetch(username)
    return data[1:-1]


def retrieve_recoms(content):
    from bin.cluster.infer import Cluster
    username = content['username']
    cluster = Cluster()
    cluster.clusters()
    result = cluster.find_similar(username)
    output = result.head()
    return output.to_json(orient='records')


def dummyvalues(n=4500):
    bubbledb = db.bubbledb()
    bubbledb.create_main_table()
    import random
    data = []
    for i in range(n):
        data1 = [f'dasykfhhh{i}89', f'2g828106{i}@gmail.com']
        data2 = ['Blockchain', 'App_Development', 'Cryptography']
        data = data1 + [random.choice(data2), random.choice(data2), random.choice(data2)]
        bubbledb.insert("accounts", data)


# print(retrieve_user({'username': 'jokhn90'}))