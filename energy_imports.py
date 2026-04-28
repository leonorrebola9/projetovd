import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
 
df = pd.read_csv('energy_imports_dependency.csv')
df = df.dropna(subset=['OBS_VALUE'])
df = df.reset_index(drop=True)  # corrigido: reset índices após dropna
 
print(f"Total de linhas: {len(df)}")
print(f"OBS_VALUE — min: {df['OBS_VALUE'].min():.2f}, max: {df['OBS_VALUE'].max():.2f}, média: {df['OBS_VALUE'].mean():.2f}")
 
# ─── 1. IQR ───────────────────────────────────────────────────────────────
Q1 = df['OBS_VALUE'].quantile(0.25)
Q3 = df['OBS_VALUE'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
mask_iqr = (df['OBS_VALUE'] < lower) | (df['OBS_VALUE'] > upper)
 
print(f"\n[IQR] Limites: [{lower:.2f}, {upper:.2f}]")
print(f"[IQR] Outliers encontrados: {mask_iqr.sum()}")
if mask_iqr.sum() > 0:
    print(df[mask_iqr][['TIME_PERIOD', 'OBS_VALUE']])
 
# ─── 2. Modified Z-Score (mais robusto para amostras pequenas) ────────────
# Usa a mediana em vez da média — mais adequado para n=21
median = df['OBS_VALUE'].median()
mad = np.median(np.abs(df['OBS_VALUE'] - median))  # Median Absolute Deviation
modified_z = 0.6745 * (df['OBS_VALUE'] - median) / mad
mask_mz = np.abs(modified_z) > 3.5  # limiar recomendado para Modified Z-Score
 
print(f"\n[Modified Z-Score] Outliers (|mz| > 3.5): {mask_mz.sum()}")
if mask_mz.sum() > 0:
    print(df[mask_mz][['TIME_PERIOD', 'OBS_VALUE']])
 
# ─── 3. Visualização ──────────────────────────────────────────────────────
x = df['TIME_PERIOD']  # corrigido: usar o ano no eixo X
 
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Dependência Energética de Portugal (2004–2024)', fontsize=13, fontweight='bold')
 
# Boxplot
axes[0].boxplot(df['OBS_VALUE'], patch_artist=True,
                boxprops=dict(facecolor='steelblue', alpha=0.6))
axes[0].set_title('Boxplot (IQR)')
axes[0].set_ylabel('Dependência Energética (%)')
axes[0].set_xticks([])
 
# Scatter com anos no eixo X (corrigido)
axes[1].scatter(x, df['OBS_VALUE'], c='steelblue', alpha=0.6, s=40, label='Normal')
if mask_iqr.sum() > 0:
    axes[1].scatter(x[mask_iqr], df['OBS_VALUE'][mask_iqr],
                    c='red', s=80, zorder=5, label=f'Outlier IQR ({mask_iqr.sum()})')
axes[1].axhline(lower, color='orange', linestyle='--', linewidth=1, label=f'Limite inf. ({lower:.1f}%)')
axes[1].axhline(upper, color='orange', linestyle='--', linewidth=1, label=f'Limite sup. ({upper:.1f}%)')
axes[1].set_title('Scatter — Método IQR')
axes[1].set_xlabel('Ano')
axes[1].set_ylabel('Dependência Energética (%)')
axes[1].legend(fontsize=8)
axes[1].tick_params(axis='x', rotation=45)
 
# Evolução temporal (substituiu o histograma — mais útil para série temporal)
axes[2].plot(x, df['OBS_VALUE'], marker='o', color='steelblue', linewidth=2, markersize=5, label='Dependência (%)')
if mask_mz.sum() > 0:
    axes[2].scatter(x[mask_mz], df['OBS_VALUE'][mask_mz],
                    c='red', s=80, zorder=5, label=f'Outlier Mod. Z ({mask_mz.sum()})')
axes[2].axhline(lower, color='orange', linestyle='--', linewidth=1, label=f'Limite inf. IQR ({lower:.1f}%)')
axes[2].axhline(upper, color='orange', linestyle='--', linewidth=1, label=f'Limite sup. IQR ({upper:.1f}%)')
axes[2].set_title('Evolução Temporal')
axes[2].set_xlabel('Ano')
axes[2].set_ylabel('Dependência Energética (%)')
axes[2].legend(fontsize=8)
axes[2].tick_params(axis='x', rotation=45)
 
plt.tight_layout()
plt.savefig('outliers_energy_dependency.png', dpi=150)
plt.show()
print("Gráfico guardado em outliers_energy_dependency.png")