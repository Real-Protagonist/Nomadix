"""
Nomadix - Tourist Clustering Model
Módulo para clustering e segmentação de dados turísticos usando Scikit-learn
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from typing import Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TouristClusteringModel:
    """Modelo para segmentação de turistas e destinos"""
    
    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.pca = None
        self.feature_names = None
        
    def prepare_features(self, df: pd.DataFrame, feature_columns: list) -> np.ndarray:
        """
        Prepara features para clustering
        
        Args:
            df: DataFrame com dados
            feature_columns: Lista de colunas para usar como features
            
        Returns:
            Array numpy com features preparadas
        """
        self.feature_names = feature_columns
        X = df[feature_columns].values
        X_scaled = self.scaler.fit_transform(X)
        logger.info(f"Features preparadas: {len(feature_columns)} colunas")
        return X_scaled
    
    def fit(self, X: np.ndarray) -> 'TouristClusteringModel':
        """
        Treina o modelo de clustering
        
        Args:
            X: Array com features
            
        Returns:
            Self
        """
        self.model.fit(X)
        logger.info(f"Modelo treinado com {self.n_clusters} clusters")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Prediz clusters para novos dados
        
        Args:
            X: Array com features
            
        Returns:
            Array com labels de clusters
        """
        return self.model.predict(X)
    
    def fit_predict(self, df: pd.DataFrame, feature_columns: list) -> np.ndarray:
        """
        Prepara, treina e prediz em uma única chamada
        
        Args:
            df: DataFrame com dados
            feature_columns: Lista de colunas para usar como features
            
        Returns:
            Array com labels de clusters
        """
        X = self.prepare_features(df, feature_columns)
        return self.model.fit_predict(X)
    
    def get_cluster_centers(self) -> np.ndarray:
        """
        Retorna os centros dos clusters
        
        Returns:
            Array com centros dos clusters
        """
        return self.scaler.inverse_transform(self.model.cluster_centers_)
    
    def get_cluster_statistics(self, df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
        """
        Calcula estatísticas por cluster
        
        Args:
            df: DataFrame com dados originais
            labels: Array com labels de clusters
            
        Returns:
            DataFrame com estatísticas por cluster
        """
        df_copy = df.copy()
        df_copy['cluster'] = labels
        
        stats = df_copy.groupby('cluster').agg({
            self.feature_names[0]: ['mean', 'count']
        })
        
        return stats
    
    def reduce_dimensions(self, X: np.ndarray, n_components: int = 2) -> np.ndarray:
        """
        Reduz dimensionalidade para visualização
        
        Args:
            X: Array com features
            n_components: Número de componentes principais
            
        Returns:
            Array com dimensões reduzidas
        """
        self.pca = PCA(n_components=n_components)
        X_reduced = self.pca.fit_transform(X)
        logger.info(f"Dimensões reduzidas para {n_components} componentes")
        return X_reduced
    
    def get_inertia(self) -> float:
        """
        Retorna a inércia do modelo (soma das distâncias quadradas)
        
        Returns:
            Valor de inércia
        """
        return self.model.inertia_
    
    def find_optimal_clusters(self, X: np.ndarray, max_clusters: int = 10) -> Dict[int, float]:
        """
        Encontra número ótimo de clusters usando método do cotovelo
        
        Args:
            X: Array com features
            max_clusters: Número máximo de clusters a testar
            
        Returns:
            Dicionário com número de clusters e inércia
        """
        inertias = {}
        
        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X)
            inertias[k] = kmeans.inertia_
        
        logger.info(f"Testados {max_clusters} números de clusters")
        return inertias
