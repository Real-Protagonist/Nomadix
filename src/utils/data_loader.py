"""
Nomadix - Data Loader
Módulo para carregamento e validação de dados turísticos
"""

import pandas as pd
import os
from typing import Optional, Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Classe para carregar e validar dados turísticos"""
    
    def __init__(self, data_path: str = "data/raw"):
        self.data_path = data_path
        
    def load_tourist_data(self, filename: str) -> Optional[pd.DataFrame]:
        """
        Carrega dados de turismo de um arquivo CSV
        
        Args:
            filename: Nome do arquivo CSV
            
        Returns:
            DataFrame com os dados ou None se houver erro
        """
        try:
            filepath = os.path.join(self.data_path, filename)
            df = pd.read_csv(filepath)
            logger.info(f"Dados carregados com sucesso: {filename}")
            return df
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {filename}")
            return None
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            return None
    
    def validate_data(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        """
        Valida se o DataFrame contém as colunas necessárias
        
        Args:
            df: DataFrame a validar
            required_columns: Lista de colunas obrigatórias
            
        Returns:
            True se válido, False caso contrário
        """
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            logger.warning(f"Colunas faltando: {missing_columns}")
            return False
        return True
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict:
        """
        Retorna um resumo dos dados
        
        Args:
            df: DataFrame para analisar
            
        Returns:
            Dicionário com estatísticas resumidas
        """
        return {
            'total_records': len(df),
            'columns': list(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.to_dict()
        }
