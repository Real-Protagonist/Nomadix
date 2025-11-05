"""
Nomadix - Visualization Utilities
Módulo para criar visualizações de dados turísticos
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, List


class DataVisualizer:
    """Classe para criar visualizações interativas"""
    
    def __init__(self):
        self.default_colors = px.colors.qualitative.Set2
    
    def create_line_chart(self, df: pd.DataFrame, x: str, y: str, 
                         title: str, color: Optional[str] = None) -> go.Figure:
        """
        Cria gráfico de linha
        
        Args:
            df: DataFrame com dados
            x: Coluna para eixo X
            y: Coluna para eixo Y
            title: Título do gráfico
            color: Coluna para coloração
            
        Returns:
            Figura Plotly
        """
        fig = px.line(df, x=x, y=y, color=color, title=title)
        fig.update_layout(
            xaxis_title=x,
            yaxis_title=y,
            hovermode='x unified'
        )
        return fig
    
    def create_bar_chart(self, df: pd.DataFrame, x: str, y: str, 
                        title: str, orientation: str = 'v') -> go.Figure:
        """
        Cria gráfico de barras
        
        Args:
            df: DataFrame com dados
            x: Coluna para eixo X
            y: Coluna para eixo Y
            title: Título do gráfico
            orientation: 'v' para vertical, 'h' para horizontal
            
        Returns:
            Figura Plotly
        """
        fig = px.bar(df, x=x, y=y, title=title, orientation=orientation)
        fig.update_layout(
            xaxis_title=x,
            yaxis_title=y
        )
        return fig
    
    def create_pie_chart(self, df: pd.DataFrame, values: str, names: str, 
                        title: str) -> go.Figure:
        """
        Cria gráfico de pizza
        
        Args:
            df: DataFrame com dados
            values: Coluna com valores
            names: Coluna com nomes
            title: Título do gráfico
            
        Returns:
            Figura Plotly
        """
        fig = px.pie(df, values=values, names=names, title=title)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    
    def create_heatmap(self, df: pd.DataFrame, x: str, y: str, z: str, 
                      title: str) -> go.Figure:
        """
        Cria mapa de calor
        
        Args:
            df: DataFrame com dados
            x: Coluna para eixo X
            y: Coluna para eixo Y
            z: Coluna com valores
            title: Título do gráfico
            
        Returns:
            Figura Plotly
        """
        pivot_table = df.pivot_table(values=z, index=y, columns=x)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=pivot_table.columns,
            y=pivot_table.index,
            colorscale='YlOrRd'
        ))
        
        fig.update_layout(title=title, xaxis_title=x, yaxis_title=y)
        return fig
    
    def create_scatter_plot(self, df: pd.DataFrame, x: str, y: str, 
                           title: str, size: Optional[str] = None,
                           color: Optional[str] = None) -> go.Figure:
        """
        Cria gráfico de dispersão
        
        Args:
            df: DataFrame com dados
            x: Coluna para eixo X
            y: Coluna para eixo Y
            title: Título do gráfico
            size: Coluna para tamanho dos pontos
            color: Coluna para coloração
            
        Returns:
            Figura Plotly
        """
        fig = px.scatter(df, x=x, y=y, size=size, color=color, title=title)
        fig.update_layout(xaxis_title=x, yaxis_title=y)
        return fig
    
    def create_area_chart(self, df: pd.DataFrame, x: str, y: str, 
                         title: str) -> go.Figure:
        """
        Cria gráfico de área
        
        Args:
            df: DataFrame com dados
            x: Coluna para eixo X
            y: Coluna para eixo Y
            title: Título do gráfico
            
        Returns:
            Figura Plotly
        """
        fig = px.area(df, x=x, y=y, title=title)
        fig.update_layout(xaxis_title=x, yaxis_title=y)
        return fig
    
    def create_box_plot(self, df: pd.DataFrame, x: str, y: str, 
                       title: str) -> go.Figure:
        """
        Cria box plot
        
        Args:
            df: DataFrame com dados
            x: Coluna para eixo X
            y: Coluna para eixo Y
            title: Título do gráfico
            
        Returns:
            Figura Plotly
        """
        fig = px.box(df, x=x, y=y, title=title)
        fig.update_layout(xaxis_title=x, yaxis_title=y)
        return fig
