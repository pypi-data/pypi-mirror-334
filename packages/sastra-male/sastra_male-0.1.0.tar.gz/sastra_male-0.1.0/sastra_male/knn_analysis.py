import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

def knn_analysis(file_path):
    """Runs KNN analysis on the given dataset and prints results."""
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Data Preprocessing
    df.drop(columns=['id', 'Unnamed: 32'], errors='ignore', inplace=True)
    df['diagnosis'] = LabelEncoder().fit_transform(df['diagnosis'])
    
    # Splitting data
    X = df.drop(columns=['diagnosis'])
    y = df['diagnosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standardization
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Finding best K
    accuracy_scores = []
    for k in range(1, 21):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train_scaled, y_train)
        y_pred = knn.predict(X_test_scaled)
        accuracy_scores.append(accuracy_score(y_test, y_pred))
    
    best_k = np.argmax(accuracy_scores) + 1  # Best K value
    knn = KNeighborsClassifier(n_neighbors=best_k)
    knn.fit(X_train_scaled, y_train)
    y_pred = knn.predict(X_test_scaled)
    accuracy_no_pca = accuracy_score(y_test, y_pred)

    # PCA for dimensionality reduction
    pca = PCA(n_components=2)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)

    # Finding best K with PCA
    accuracy_scores_pca = []
    for k in range(1, 21):
        knn_pca = KNeighborsClassifier(n_neighbors=k)
        knn_pca.fit(X_train_pca, y_train)
        y_pred_pca = knn_pca.predict(X_test_pca)
        accuracy_scores_pca.append(accuracy_score(y_test, y_pred_pca))
    
    best_k_pca = np.argmax(accuracy_scores_pca) + 1
    knn_pca = KNeighborsClassifier(n_neighbors=best_k_pca)
    knn_pca.fit(X_train_pca, y_train)
    y_pred_pca = knn_pca.predict(X_test_pca)
    accuracy_with_pca = accuracy_score(y_test, y_pred_pca)

    # Display results
    print("\n--- KNN Analysis Results ---")
    print(f"Best K without PCA: {best_k}, Accuracy: {accuracy_no_pca:.4f}")
    print(f"Best K with PCA: {best_k_pca}, Accuracy: {accuracy_with_pca:.4f}")
