"""
Gerador de Dados de Exemplo para Nomadix
Cria datasets sintéticos para demonstração do sistema
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configurações
np.random.seed(42)

# Define províncias de Angola
provincias = ['Luanda', 'Benguela', 'Huíla', 'Namibe', 'Cabinda', 'Huambo', 'Cuanza Sul']

# Período de dados
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)
dates = pd.date_range(start=start_date, end=end_date, freq='M')

# Capacidade base por província
capacidade_base = {
    'Luanda': 15000,
    'Benguela': 8000,
    'Huíla': 6000,
    'Namibe': 5000,
    'Cabinda': 4500,
    'Huambo': 5500,
    'Cuanza Sul': 4000
}

# Gera dados turísticos
data = []

for date in dates:
    for provincia in provincias:
        base = capacidade_base[provincia]
        
        # Adiciona sazonalidade (pico no verão angolano)
        seasonal_factor = 1 + 0.3 * np.sin((date.month - 3) * np.pi / 6)
        
        # Adiciona tendência de crescimento
        trend_factor = 1 + 0.05 * (date.year - 2020)
        
        # Adiciona ruído aleatório
        noise = np.random.normal(1, 0.15)
        
        # Calcula visitantes
        visitantes = int(base * seasonal_factor * trend_factor * noise)
        
        # Calcula outras métricas
        gasto_medio = np.random.uniform(50, 200)
        receita = visitantes * gasto_medio
        estadia_media = np.random.uniform(2, 8)
        satisfacao = np.random.uniform(3.0, 5.0)
        taxa_ocupacao = min(np.random.uniform(0.5, 0.95), 1.0)
        
        # Infraestrutura
        hoteis = int(np.random.uniform(10, 80))
        restaurantes = int(np.random.uniform(30, 150))
        
        data.append({
            'data': date,
            'provincia': provincia,
            'visitantes': visitantes,
            'receita_usd': round(receita, 2),
            'gasto_medio_usd': round(gasto_medio, 2),
            'estadia_media_dias': round(estadia_media, 2),
            'satisfacao': round(satisfacao, 2),
            'taxa_ocupacao': round(taxa_ocupacao, 3),
            'hoteis': hoteis,
            'restaurantes': restaurantes,
            'temperatura_media_c': round(np.random.uniform(22, 32), 1)
        })

# Cria DataFrame
df = pd.DataFrame(data)

# Salva em CSV
df.to_csv('data/raw/turismo_angola_2020_2024.csv', index=False, encoding='utf-8')

print(f"✅ Dataset criado: {len(df)} registros")
print(f"📅 Período: {df['data'].min()} a {df['data'].max()}")
print(f"🗺️ Províncias: {', '.join(provincias)}")
print(f"💾 Arquivo salvo em: data/raw/turismo_angola_2020_2024.csv")

# Cria dataset agregado anual
df_anual = df.copy()
df_anual['ano'] = df_anual['data'].dt.year

df_agregado = df_anual.groupby(['ano', 'provincia']).agg({
    'visitantes': 'sum',
    'receita_usd': 'sum',
    'gasto_medio_usd': 'mean',
    'estadia_media_dias': 'mean',
    'satisfacao': 'mean',
    'taxa_ocupacao': 'mean',
    'hoteis': 'mean',
    'restaurantes': 'mean'
}).reset_index()

df_agregado = df_agregado.round(2)

# Salva agregado
df_agregado.to_csv('data/processed/turismo_angola_anual.csv', index=False, encoding='utf-8')

print(f"\n✅ Dataset anual criado: {len(df_agregado)} registros")
print(f"💾 Arquivo salvo em: data/processed/turismo_angola_anual.csv")

# Estatísticas
print("\n📊 Estatísticas Gerais:")
print(f"Total de visitantes (2020-2024): {df['visitantes'].sum():,.0f}")
print(f"Receita total: ${df['receita_usd'].sum():,.2f}")
print(f"Satisfação média: {df['satisfacao'].mean():.2f}/5.0")
print(f"Estadia média: {df['estadia_media_dias'].mean():.1f} dias")
