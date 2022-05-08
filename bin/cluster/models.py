from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from gensim.models import Word2Vec

# sample function
class VecModel:  
    def __init__(self):
        self.weights = 'weights.embedding'


    def make_dataset(n=4500):
        sample = [('Web_Development','Machine_learning','Cybersecurity'),
                ('Blockchain', 'App_Development', 'Cryptography'), 
                ('Cryptography', 'Blockchain', 'Cybersecurity'), 
                ('App_Development', 'Web_Development', 'Machine_Learning')]
                
        data = []
        for i in range(n):
            data.append(sample[i%len(sample)])
        return data


    def make_model(self, data):
        model = Word2Vec(data, min_count = 1)
        model.save(self.weights)


    def infer_most_similar(self, interests):
        model = Word2Vec.load(self.weights)
        most_similar = []
        for interest in interests:
            most_similar.append(model.wv.most_similar(positive = [interest], topn = 3))
        return most_similar


    def infer(self, interest):
        model = Word2Vec.load(self.weights)
        vector = []
        try:
            vector = model.wv.get_mean_vector(interest, weights=[1.4, 1.0, 0.6], pre_normalize=True, post_normalize=True, ignore_missing=True)
        except:
            pass
        return vector


    def dbscan(self, X, debug=False):
        X = StandardScaler().fit_transform(X)
        dbscan = DBSCAN(eps=2, min_samples=2).fit(X)    ##replace X with database
        labels = dbscan.labels_

        if debug:
            print(labels)
            n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
            n_noise_ = list(labels).count(-1)
            print(f"Estimated number of clusters: {n_clusters_}")
            print(f"Estimated number of noise points: {n_noise_}")
            print(f"Silhouette Coefficient: {metrics.silhouette_score(X, labels)}")

        return labels



      

  
  