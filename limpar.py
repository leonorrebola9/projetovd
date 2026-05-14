import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("data/eu27_energy_dataset.csv", sep=";")

# ── 1. Remover coluna com muitos nulos ────────────────────────────────────────
# Nota: nome da coluna gerado automaticamente com base no setor "Off-shore"
off_shore_col = [c for c in df.columns if 'off' in c.lower() and 'shore' in c.lower()]
if off_shore_col:
    df = df.drop(columns=off_shore_col)
    print(f"Coluna(s) removida(s): {off_shore_col}")

# ── 2. Converter zeros falsos para NaN ────────────────────────────────────────
colunas_zeros_falsos = ['public_rd_investment', 'private_rd_investment', 'clean_energy_patents']
df[colunas_zeros_falsos] = df[colunas_zeros_falsos].replace(0, np.nan)

# ── 3. Preencher NaN com média do país ───────────────────────────────────────
colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

for col in colunas_numericas:
    media_pais = df.groupby('country')[col].transform('mean')
    df[col] = df[col].fillna(media_pais)

# ── 4. Preencher NaN restantes com média global ───────────────────────────────
# (países que não têm qualquer dado numa coluna, ex: Bulgária em public_rd_investment)
for col in colunas_numericas:
    df[col] = df[col].fillna(df[col].mean())

# ── 5. Substituir outliers pela média do país ─────────────────────────────────
colunas_outliers = [c for c in colunas_numericas if c != 'year']

for col in colunas_outliers:
    z_col = df[col].groupby(df['country']).transform(
        lambda x: np.abs(stats.zscore(x, nan_policy='omit'))
    )
    mask = z_col > 3
    media_pais = df[col].groupby(df['country']).transform('mean')
    df.loc[mask, col] = media_pais[mask]

# ── 6. Guardar ────────────────────────────────────────────────────────────────
df.to_csv("energy_dataset_clean1.csv", index=False, sep=";")
print("Ficheiro guardado")
print(f"Shape: {df.shape}")
print(f"Nulos restantes: {df.isnull().sum().sum()}")
print(f"Colunas GHG: {[c for c in df.columns if 'ghg' in c]}")
