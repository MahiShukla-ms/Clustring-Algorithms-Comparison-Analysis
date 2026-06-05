
import pandas as pd
import numpy as np
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
    adjusted_rand_score
)


def evaluate_clustering(X: np.ndarray, cluster_labels: np.ndarray, 
                       true_labels: np.ndarray = None, algorithm_name: str = ""):
    """
    Evaluate clustering quality using multiple metrics.
    
    Args:
        X: Feature data
        cluster_labels: Predicted cluster labels
        true_labels: Ground truth labels (optional)
        algorithm_name: Name of the clustering algorithm
        
    Returns:
        Dictionary with evaluation metrics
    """
    results = {
        "Algorithm": algorithm_name,
        "Clusters": len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0),
    }
    
    # Only compute metrics if we have more than 1 cluster
    if len(set(cluster_labels)) > 1 and not (-1 in cluster_labels and len(set(cluster_labels)) == 2):
        try:
            results["Silhouette Score"] = round(
                silhouette_score(X, cluster_labels), 3
            )
        except:
            results["Silhouette Score"] = None
            
        try:
            results["Davies-Bouldin"] = round(
                davies_bouldin_score(X, cluster_labels), 3
            )
        except:
            results["Davies-Bouldin"] = None
            
        try:
            results["Calinski-Harabasz"] = round(
                calinski_harabasz_score(X, cluster_labels), 1
            )
        except:
            results["Calinski-Harabasz"] = None
    else:
        results["Silhouette Score"] = None
        results["Davies-Bouldin"] = None
        results["Calinski-Harabasz"] = None
        
    # If ground truth available, compute adjusted Rand index
    if true_labels is not None:
        try:
            results["Adjusted Rand Index"] = round(
                adjusted_rand_score(true_labels, cluster_labels), 3
            )
        except:
            results["Adjusted Rand Index"] = None
    
    return results


def save_cluster_metrics(results: pd.DataFrame, 
                        output_path: str = "data/cluster_metrics.csv") -> None:
    """Save evaluation metrics to CSV file."""
    results.to_csv(output_path, index=False)
    print(f"Metrics saved to {output_path}")