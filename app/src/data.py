# Sample, To be replaced with postgres
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler


def get():
    centers = [[1, 1], [-1, -1], [1, -1]]
    X, labels_true = make_blobs(
        n_samples=750, centers=centers, cluster_std=0.4, random_state=0
    )

    X = StandardScaler().fit_transform(X)
    return X, labels_true