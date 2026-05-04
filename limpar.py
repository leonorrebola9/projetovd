import pandas as pd
import numpy as np
from scipy import stats

'''
df = pd.read_csv("data/eu27_energy_dataset_2004_2023.csv", sep=";")

# Remover coluna com muitos nulos
df = df.drop(columns=["ghg_off-shore_kt_co2eq"])

# Função de média ponderada
def weighted_mean(series, weights):
    mask = series.notna()
    return np.average(series[mask], weights=weights[mask])

# Preencher nulos
for col in df.columns:
    if df[col].isnull().sum() > 0 and df[col].dtype != "object":
        media_pond = weighted_mean(df[col], df["population"])
        df[col] = df[col].fillna(media_pond)

# Guardar novo CSV
df.to_csv("dados_limpos.csv", index=False)
'''



df = pd.read_csv("dados_limpos.csv")
'''
# Total de nulos no dataset inteiro
total_nulos = df.isnull().sum().sum()
print(total_nulos)

# Nulos por coluna
print(df.isnull().sum())
'''


# 1. Calcular o Z-score
# O .dropna() ou preenchimento de nulos é importante antes disto


# 2. Selecionar apenas as colunas numéricas (int e float)
df_numerico = df.select_dtypes(include=[np.number])

# 3. Calcular o Z-score absoluto para todas as colunas numéricas
z_scores = np.abs(stats.zscore(df_numerico))

# 4. Criar uma máscara booleana: True se o Z-score > 3 em qualquer coluna
# (O .any(axis=1) verifica se acontece em pelo menos uma coluna da linha)
mask_outliers = (z_scores > 3).any(axis=1)

# 5. Mostrar as linhas que contêm outliers
outliers_detetados = df[mask_outliers]

print(f"Total de linhas com pelo menos um outlier: {len(outliers_detetados)}")
print(outliers_detetados)

# Contar True (outliers) por coluna
contagem_outliers = (z_scores > 3).sum()

print("Outliers por coluna:")
print(contagem_outliers[contagem_outliers > 0])


