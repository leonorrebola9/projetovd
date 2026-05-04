import pandas as pd
import numpy as np
from scipy import stats

# ── Limpeza de nulos ──────────────────────────────────────────────────────────
df = pd.read_csv("data/eu27_energy_dataset_2004_2023.csv", sep=";")

# Remover coluna com muitos nulos
df = df.drop(columns=["ghg_off-shore_kt_co2eq"])

# Função de média ponderada
def weighted_mean(series, weights):
    mask = series.notna()
    return np.average(series[mask], weights=weights[mask])

# Preencher nulos com média ponderada pela população
for col in df.columns:
    if df[col].isnull().sum() > 0 and df[col].dtype != "object":
        media_pond = weighted_mean(df[col], df["population"])
        df[col] = df[col].fillna(media_pond)

df.to_csv("dados_limpos.csv", index=False, sep=";")

# ── Deteção e substituição de outliers ───────────────────────────────────────
df = pd.read_csv("dados_limpos.csv", sep=";")

# Separar colunas numéricas (excluir country e year)
colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
colunas_numericas = [c for c in colunas_numericas if c != 'year']

df_limpo = df.copy()

for col in colunas_numericas:
    z_col = df[col].groupby(df['country']).transform(
        lambda x: np.abs(stats.zscore(x, nan_policy='omit'))
    )
    mask = z_col > 3
    medias_pais = df[col].groupby(df['country']).transform('mean')
    df_limpo.loc[mask, col] = medias_pais[mask]

# Mostrar resumo
df_numerico = df[colunas_numericas]
z_scores = df_numerico.groupby(df['country']).transform(
    lambda x: np.abs(stats.zscore(x, nan_policy='omit'))
)
contagem_outliers = (z_scores > 3).sum()
print(f"Total de linhas com pelo menos um outlier: {(z_scores > 3).any(axis=1).sum()}")
print("Outliers por coluna:")
print(contagem_outliers[contagem_outliers > 0])

df_limpo.to_csv('energy_dataset_clean.csv', index=False, sep=';')
print("Ficheiro guardado: energy_dataset_clean.csv")