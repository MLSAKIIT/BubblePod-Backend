# Sample, To be replaced with postgres
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

def get():
    X, labels_true = make_blobs(n_samples=750)

    X = StandardScaler().fit_transform(X)
    return X, labels_true