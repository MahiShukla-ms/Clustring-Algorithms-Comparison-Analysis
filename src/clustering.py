
import numpy as np
import pandas as pd
import time
from sklearn.cluster import (
    KMeans,
    MiniBatchKMeans,
    DBSCAN,
    AgglomerativeClustering,
    SpectralClustering,
)
from sklearn.mixture import GaussianMixture


def fit_kmeans(X: np.ndarray, n_clusters: int = 10, random_state: int = 42):
    """
    K-Means Clustering
    
    Fast, scalable partitional clustering.
    Works best with spherical clusters.
    """
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    start = time.time()
    model.fit(X)
    exec_time = time.time() - start
    return model, exec_time, model.labels_


def fit_minibatch_kmeans(X: np.ndarray, n_clusters: int = 10, random_state: int = 42):
    """
    Mini-Batch K-Means
    
    Faster alternative for very large datasets.
    Uses mini-batches to reduce computation.
    """
    model = MiniBatchKMeans(n_clusters=n_clusters, batch_size=1000, random_state=random_state)
    start = time.time()
    model.fit(X)
    exec_time = time.time() - start
    return model, exec_time, model.labels_


def fit_agglomerative(X: np.ndarray, n_clusters: int = 10):
    """
    Agglomerative Clustering
    
    Hierarchical clustering using bottom-up approach.
    Good for small to medium datasets.
    """
    model = AgglomerativeClustering(n_clusters=n_clusters)
    start = time.time()
    labels = model.fit_predict(X)
    exec_time = time.time() - start
    return model, exec_time, labels


def fit_dbscan(X: np.ndarray, eps: float = 3.0, min_samples: int = 5):
    """
    DBSCAN (Density-Based Spatial Clustering)
    
    Finds clusters based on density.
    Can identify outliers (labeled as -1).
    Parameter sensitive: requires careful eps tuning.
    """
    model = DBSCAN(eps=eps, min_samples=min_samples)
    start = time.time()
    labels = model.fit_predict(X)
    exec_time = time.time() - start
    return model, exec_time, labels


def fit_gaussian_mixture(X: np.ndarray, n_components: int = 10, random_state: int = 42):
    """
    Gaussian Mixture Model
    
    Probabilistic clustering assuming Gaussian distributions.
    Good for soft clustering (probabilities instead of hard labels).
    """
    model = GaussianMixture(n_components=n_components, random_state=random_state)
    start = time.time()
    labels = model.fit_predict(X)
    exec_time = time.time() - start
    return model, exec_time, labels


def fit_spectral_clustering(X: np.ndarray, n_clusters: int = 10, random_state: int = 42):
    """
    Spectral Clustering
    
    Graph-based clustering that can handle complex cluster shapes.
    More computationally expensive but very effective.
    """
    model = SpectralClustering(
        n_clusters=n_clusters,
        affinity="nearest_neighbors",
        random_state=random_state,
        n_init=10
    )
    start = time.time()
    labels = model.fit_predict(X)
    exec_time = time.time() - start
    return model, exec_time, labels


def get_algorithm(name: str, n_clusters: int = 10, eps: float = 3.0):
    """
    Get clustering algorithm by name.
    
    Returns: (fit_function, algorithm_name)
    """
    algorithms = {
        "K-Means": lambda X: fit_kmeans(X, n_clusters),
        "Mini-Batch K-Means": lambda X: fit_minibatch_kmeans(X, n_clusters),
        "DBSCAN": lambda X: fit_dbscan(X, eps),
        "Agglomerative": lambda X: fit_agglomerative(X, n_clusters),
        "Gaussian Mixture": lambda X: fit_gaussian_mixture(X, n_clusters),
        "Spectral": lambda X: fit_spectral_clustering(X, n_clusters),
    }
    
    if name not in algorithms:
        raise ValueError(f"Unknown algorithm: {name}. Choose from {list(algorithms.keys())}")
    
    return algorithms[name]