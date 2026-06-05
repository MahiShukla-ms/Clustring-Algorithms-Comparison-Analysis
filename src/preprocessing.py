import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def load_dataset(path: str = "Dataset/fashion-mnist_test.csv") -> pd.DataFrame:
    """Load the Fashion MNIST CSV dataset."""
    df = pd.read_csv(path)
    print(f"Dataset loaded: {df.shape}")
    return df


def create_class_distribution_csv(df: pd.DataFrame, output_path: str = " Dataset/class_distribution.csv") -> pd.DataFrame:
    """Save label counts to a CSV for dashboard use."""
    summary = df["Label"].value_counts().sort_index().rename_axis("Label").reset_index(name="Count")
    summary.to_csv(output_path, index=False)
    return summary


def extract_features(df: pd.DataFrame) -> np.ndarray:
    """
    Extract pixel features from the dataset.
    
    Fashion-MNIST: 28x28 images = 784 pixel features
    Each pixel has value 0-255 (grayscale intensity)
    
    Returns:
        Numpy array of shape (n_samples, 784)
    """
    features = df.drop(columns=["label"]).values
    print(f"Extracted features shape: {features.shape}")
    return features


def standardize_features(X: np.ndarray) -> np.ndarray:
    """
    Scale pixel values to zero mean and unit variance.
    
    Why? Algorithms like K-Means work better with standardized features
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print(f"Features standardized. Mean: {X_scaled.mean():.2f}, Std: {X_scaled.std():.2f}")
    return X_scaled


def reduce_dimensions(X: np.ndarray, n_components: int = 2, random_state: int = 42):
    """
    Reduce dimensionality using PCA.
    
    Fashion-MNIST: 784 dimensions → n_components (usually 2 for visualization)
    
    Args:
        X: Input data (n_samples, 784)
        n_components: Number of principal components to keep
        
    Returns:
        X_reduced: Reduced data (n_samples, n_components)
        pca: Fitted PCA object
    """
    pca = PCA(n_components=n_components, random_state=random_state)
    X_reduced = pca.fit_transform(X)
    
    variance_explained = sum(pca.explained_variance_ratio_)
    print(f"PCA: 784 dimensions → {n_components} dimensions")
    print(f"Variance explained: {variance_explained:.2%}")
    
    return X_reduced, pca