import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

'''
df = pd.read_csv('complete_energy_balances_portugal.csv')
df = df.dropna(subset=['OBS_VALUE'])

print(f"Total de linhas: {len(df)}")
print(f"OBS_VALUE — min: {df['OBS_VALUE'].min():.2f}, max: {df['OBS_VALUE'].max():.2f}, média: {df['OBS_VALUE'].mean():.2f}")

# ─── 1. IQR ───────────────────────────────────────────────────────────────
Q1 = df['OBS_VALUE'].quantile(0.25)
Q3 = df['OBS_VALUE'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers_iqr = df[(df['OBS_VALUE'] < lower) | (df['OBS_VALUE'] > upper)]
print(f"\n[IQR] Limites: [{lower:.2f}, {upper:.2f}]")
print(f"[IQR] Outliers encontrados: {len(outliers_iqr)}")

# ─── 2. Z-Score ───────────────────────────────────────────────────────────
z_scores = np.abs(stats.zscore(df['OBS_VALUE']))
outliers_z = df[z_scores > 3]
print(f"\n[Z-Score] Outliers (|z| > 3): {len(outliers_z)}")

# ─── 3. Visualização ──────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Deteção de Outliers — OBS_VALUE (Portugal Energy Balances)', fontsize=13, fontweight='bold')

# Boxplot
axes[0].boxplot(df['OBS_VALUE'], patch_artist=True,
                boxprops=dict(facecolor='steelblue', alpha=0.6))
axes[0].set_title('Boxplot (IQR)')
axes[0].set_ylabel('OBS_VALUE')

# Scatter
mask_iqr = (df['OBS_VALUE'] < lower) | (df['OBS_VALUE'] > upper)
axes[1].scatter(range(len(df)), df['OBS_VALUE'], c='steelblue', alpha=0.4, s=8, label='Normal')
axes[1].scatter(df.index[mask_iqr], df['OBS_VALUE'][mask_iqr], c='red', s=40, zorder=5, label=f'Outlier IQR ({mask_iqr.sum()})')
axes[1].axhline(lower, color='orange', linestyle='--', linewidth=1, label=f'Limite inf. ({lower:.0f})')
axes[1].axhline(upper, color='orange', linestyle='--', linewidth=1, label=f'Limite sup. ({upper:.0f})')
axes[1].set_title('Scatter — Método IQR')
axes[1].legend(fontsize=7)

# Histograma
mask_z = z_scores > 3
axes[2].hist(df['OBS_VALUE'][~mask_z], bins=40, color='steelblue', alpha=0.7, label='Normal')
axes[2].hist(df['OBS_VALUE'][mask_z],  bins=40, color='red',       alpha=0.9, label=f'Outlier Z-Score ({mask_z.sum()})')
axes[2].set_title('Histograma — Z-Score')
axes[2].legend()

plt.tight_layout()
plt.savefig('outliers.png', dpi=150)
plt.show()
print("Gráfico guardado em outliers.png")

'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('consumo_de_energia_primaria_total_e_por_tipo_de_fonte_de_energia.csv')
df = df.dropna(subset=['Total'])

print(f"Total de linhas: {len(df)}")
print(f"Total — min: {df['Total'].min():.2f}, max: {df['Total'].max():.2f}, média: {df['Total'].mean():.2f}")

# ─── 1. IQR ───────────────────────────────────────────────────────────────
Q1 = df['Total'].quantile(0.25)
Q3 = df['Total'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers_iqr = df[(df['Total'] < lower) | (df['Total'] > upper)]
print(f"\n[IQR] Limites: [{lower:.2f}, {upper:.2f}]")
print(f"[IQR] Outliers encontrados: {len(outliers_iqr)}")

# ─── 2. Z-Score ───────────────────────────────────────────────────────────
z_scores = np.abs(stats.zscore(df['Total']))
outliers_z = df[z_scores > 3]
print(f"\n[Z-Score] Outliers (|z| > 3): {len(outliers_z)}")

# ─── 3. Visualização ──────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Deteção de Outliers — Total (Portugal Energy Balances)', fontsize=13, fontweight='bold')

# Boxplot
axes[0].boxplot(df['Total'], patch_artist=True,
                boxprops=dict(facecolor='steelblue', alpha=0.6))
axes[0].set_title('Boxplot (IQR)')
axes[0].set_ylabel('Total')

# Scatter
mask_iqr = (df['Total'] < lower) | (df['Total'] > upper)
axes[1].scatter(range(len(df)), df['Total'], c='steelblue', alpha=0.4, s=8, label='Normal')
axes[1].scatter(df.index[mask_iqr], df['Total'][mask_iqr], c='red', s=40, zorder=5, label=f'Outlier IQR ({mask_iqr.sum()})')
axes[1].axhline(lower, color='orange', linestyle='--', linewidth=1, label=f'Limite inf. ({lower:.0f})')
axes[1].axhline(upper, color='orange', linestyle='--', linewidth=1, label=f'Limite sup. ({upper:.0f})')
axes[1].set_title('Scatter — Método IQR')
axes[1].legend(fontsize=7)

# Histograma
mask_z = z_scores > 3
axes[2].hist(df['Total'][~mask_z], bins=40, color='steelblue', alpha=0.7, label='Normal')
axes[2].hist(df['Total'][mask_z],  bins=40, color='red',       alpha=0.9, label=f'Outlier Z-Score ({mask_z.sum()})')
axes[2].set_title('Histograma — Z-Score')
axes[2].legend()

plt.tight_layout()
plt.savefig('outliers.png', dpi=150)
plt.show()
print("Gráfico guardado em outliers.png")
