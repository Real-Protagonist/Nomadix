"""
Nomadix - Data Processor
Módulo para processamento e transformação de dados turísticos
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Classe para processar e transformar dados turísticos"""
    
    def __init__(self):
        pass
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpa dados removendo duplicatas e valores nulos
        
        Args:
            df: DataFrame a ser limpo
            
        Returns:
            DataFrame limpo
        """
        initial_rows = len(df)
        
        # Remove duplicatas
        df = df.drop_duplicates()
        
        # Remove linhas com muitos valores nulos (>50%)
        threshold = len(df.columns) * 0.5
        df = df.dropna(thresh=threshold)
        
        final_rows = len(df)
        logger.info(f"Limpeza concluída: {initial_rows} -> {final_rows} registros")
        
        return df
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        """
        Trata valores ausentes
        
        Args:
            df: DataFrame com valores ausentes
            strategy: Estratégia para preenchimento ('mean', 'median', 'forward', 'drop')
            
        Returns:
            DataFrame com valores tratados
        """
        df_copy = df.copy()
        
        numeric_columns = df_copy.select_dtypes(include=[np.number]).columns
        
        if strategy == 'mean':
            df_copy[numeric_columns] = df_copy[numeric_columns].fillna(df_copy[numeric_columns].mean())
        elif strategy == 'median':
            df_copy[numeric_columns] = df_copy[numeric_columns].fillna(df_copy[numeric_columns].median())
        elif strategy == 'forward':
            df_copy = df_copy.fillna(method='ffill')
        elif strategy == 'drop':
            df_copy = df_copy.dropna()
        
        logger.info(f"Valores ausentes tratados com estratégia: {strategy}")
        return df_copy
    
    def aggregate_by_period(self, df: pd.DataFrame, date_column: str, 
                           freq: str = 'M') -> pd.DataFrame:
        """
        Agrega dados por período temporal
        
        Args:
            df: DataFrame com dados
            date_column: Nome da coluna de data
            freq: Frequência de agregação ('D', 'W', 'M', 'Q', 'Y')
            
        Returns:
            DataFrame agregado
        """
        df_copy = df.copy()
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        df_copy = df_copy.set_index(date_column)
        
        # Agrega dados numéricos
        numeric_columns = df_copy.select_dtypes(include=[np.number]).columns
        aggregated = df_copy[numeric_columns].resample(freq).sum()
        
        logger.info(f"Dados agregados por período: {freq}")
        return aggregated.reset_index()
    
    def calculate_growth_rate(self, df: pd.DataFrame, column: str) -> pd.Series:
        """
        Calcula taxa de crescimento percentual
        
        Args:
            df: DataFrame com dados
            column: Coluna para calcular crescimento
            
        Returns:
            Series com taxas de crescimento
        """
        return df[column].pct_change() * 100
    
    def normalize_data(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """
        Normaliza dados (0-1 scale)
        
        Args:
            df: DataFrame com dados
            columns: Colunas a normalizar
            
        Returns:
            DataFrame com dados normalizados
        """
        df_copy = df.copy()
        
        for col in columns:
            if col in df_copy.columns:
                min_val = df_copy[col].min()
                max_val = df_copy[col].max()
                df_copy[col] = (df_copy[col] - min_val) / (max_val - min_val)
        
        logger.info(f"Dados normalizados: {columns}")
        return df_copy
    
    def create_time_features(self, df: pd.DataFrame, date_column: str) -> pd.DataFrame:
        """
        Cria features temporais a partir de uma coluna de data
        
        Args:
            df: DataFrame com dados
            date_column: Nome da coluna de data
            
        Returns:
            DataFrame com features temporais adicionadas
        """
        df_copy = df.copy()
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        
        df_copy['ano'] = df_copy[date_column].dt.year
        df_copy['mes'] = df_copy[date_column].dt.month
        df_copy['trimestre'] = df_copy[date_column].dt.quarter
        df_copy['dia_semana'] = df_copy[date_column].dt.dayofweek
        df_copy['semana_ano'] = df_copy[date_column].dt.isocalendar().week
        
        logger.info("Features temporais criadas")
        return df_copy
