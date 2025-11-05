"""
Nomadix - Tourist Forecasting Model
Módulo para previsões de séries temporais usando Prophet
"""

import pandas as pd
import numpy as np
from prophet import Prophet
from typing import Dict, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TouristForecastingModel:
    """Modelo para previsão de tendências turísticas"""
    
    def __init__(self, 
                 yearly_seasonality: bool = True,
                 weekly_seasonality: bool = False,
                 daily_seasonality: bool = False):
        """
        Inicializa o modelo Prophet
        
        Args:
            yearly_seasonality: Se deve considerar sazonalidade anual
            weekly_seasonality: Se deve considerar sazonalidade semanal
            daily_seasonality: Se deve considerar sazonalidade diária
        """
        self.model = Prophet(
            yearly_seasonality=yearly_seasonality,
            weekly_seasonality=weekly_seasonality,
            daily_seasonality=daily_seasonality
        )
        self.is_fitted = False
        
    def prepare_data(self, df: pd.DataFrame, date_column: str, 
                    value_column: str) -> pd.DataFrame:
        """
        Prepara dados no formato do Prophet (ds, y)
        
        Args:
            df: DataFrame com dados
            date_column: Nome da coluna de data
            value_column: Nome da coluna com valores
            
        Returns:
            DataFrame no formato Prophet
        """
        prophet_df = pd.DataFrame({
            'ds': pd.to_datetime(df[date_column]),
            'y': df[value_column]
        })
        
        logger.info(f"Dados preparados: {len(prophet_df)} registros")
        return prophet_df
    
    def fit(self, df: pd.DataFrame) -> 'TouristForecastingModel':
        """
        Treina o modelo com dados históricos
        
        Args:
            df: DataFrame no formato Prophet (ds, y)
            
        Returns:
            Self
        """
        self.model.fit(df)
        self.is_fitted = True
        logger.info("Modelo Prophet treinado com sucesso")
        return self
    
    def predict(self, periods: int, freq: str = 'M') -> pd.DataFrame:
        """
        Gera previsões para períodos futuros
        
        Args:
            periods: Número de períodos para prever
            freq: Frequência ('D', 'W', 'M', 'Q', 'Y')
            
        Returns:
            DataFrame com previsões
        """
        if not self.is_fitted:
            raise ValueError("Modelo precisa ser treinado antes de fazer previsões")
        
        future = self.model.make_future_dataframe(periods=periods, freq=freq)
        forecast = self.model.predict(future)
        
        logger.info(f"Previsões geradas para {periods} períodos")
        return forecast
    
    def get_forecast_summary(self, forecast: pd.DataFrame, 
                            last_n: Optional[int] = None) -> pd.DataFrame:
        """
        Retorna resumo das previsões
        
        Args:
            forecast: DataFrame com previsões do Prophet
            last_n: Número de últimas previsões a retornar
            
        Returns:
            DataFrame com resumo simplificado
        """
        columns = ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
        summary = forecast[columns].copy()
        
        summary.columns = ['data', 'previsao', 'limite_inferior', 'limite_superior']
        
        if last_n:
            summary = summary.tail(last_n)
        
        return summary
    
    def get_components(self, forecast: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Extrai componentes da previsão (tendência, sazonalidade)
        
        Args:
            forecast: DataFrame com previsões do Prophet
            
        Returns:
            Dicionário com componentes
        """
        components = {}
        
        if 'trend' in forecast.columns:
            components['tendencia'] = forecast[['ds', 'trend']].copy()
        
        if 'yearly' in forecast.columns:
            components['sazonalidade_anual'] = forecast[['ds', 'yearly']].copy()
        
        if 'weekly' in forecast.columns:
            components['sazonalidade_semanal'] = forecast[['ds', 'weekly']].copy()
        
        logger.info(f"Componentes extraídos: {list(components.keys())}")
        return components
    
    def add_regressor(self, name: str, df: pd.DataFrame) -> 'TouristForecastingModel':
        """
        Adiciona regressor customizado ao modelo
        
        Args:
            name: Nome do regressor
            df: DataFrame com dados do regressor
            
        Returns:
            Self
        """
        if self.is_fitted:
            logger.warning("Modelo já foi treinado. Crie um novo modelo para adicionar regressores.")
            return self
        
        self.model.add_regressor(name)
        logger.info(f"Regressor adicionado: {name}")
        return self
    
    def add_country_holidays(self, country: str = 'AO') -> 'TouristForecastingModel':
        """
        Adiciona feriados de um país ao modelo
        
        Args:
            country: Código ISO do país (AO para Angola)
            
        Returns:
            Self
        """
        if self.is_fitted:
            logger.warning("Modelo já foi treinado. Crie um novo modelo para adicionar feriados.")
            return self
        
        self.model.add_country_holidays(country_name=country)
        logger.info(f"Feriados de {country} adicionados ao modelo")
        return self
    
    def calculate_metrics(self, actual: pd.DataFrame, forecast: pd.DataFrame) -> Dict[str, float]:
        """
        Calcula métricas de performance
        
        Args:
            actual: DataFrame com valores reais (ds, y)
            forecast: DataFrame com previsões
            
        Returns:
            Dicionário com métricas (MAE, RMSE, MAPE)
        """
        merged = actual.merge(forecast[['ds', 'yhat']], on='ds', how='inner')
        
        mae = np.mean(np.abs(merged['y'] - merged['yhat']))
        rmse = np.sqrt(np.mean((merged['y'] - merged['yhat']) ** 2))
        mape = np.mean(np.abs((merged['y'] - merged['yhat']) / merged['y'])) * 100
        
        metrics = {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape
        }
        
        logger.info(f"Métricas calculadas: MAE={mae:.2f}, RMSE={rmse:.2f}, MAPE={mape:.2f}%")
        return metrics
