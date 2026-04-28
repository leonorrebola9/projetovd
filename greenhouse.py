import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ─── Carregar dados ────────────────────────────────────────────────────────────
df = pd.read_csv('greenhouse_gas_emissions_by_source_sector.csv')
df = df.dropna(subset=['OBS_VALUE']).reset_index(drop=True)
df = df[(df['TIME_PERIOD'] >= 2004) & (df['TIME_PERIOD'] <= 2024)]

# Nomes legíveis para poluentes e setores
POLLUTANT_LABELS = {
    'GHG':      'GHG (CO₂ equivalente)',
    'CO2':      'CO₂',
    'CH4':      'CH₄ (Metano)',
    'CH4_CO2E': 'CH₄ (CO₂ equiv.)',
    'N2O':      'N₂O (Óxido nitroso)',
}
SECTOR_LABELS = {
    'CRF1':       'Energia (total)',
    'CRF1A':      'Combustão de combustíveis',
    'CRF1A1':     'Indústrias energéticas',
    'TOTX4_MEMO': 'Total (excl. LULUCF)',
    'TOTXMEMO':   'Total (excl. memo items)',
}

# ─── Funções de deteção de outliers ───────────────────────────────────────────
def iqr_outliers(series):
    Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    mask = (series < lower) | (series > upper)
    return mask, lower, upper

def modified_zscore_outliers(series, threshold=3.5):
    median = series.median()
    mad = np.median(np.abs(series - median))
    if mad == 0:
        return pd.Series(False, index=series.index), median, median
    mz = 0.6745 * (series - median) / mad
    return np.abs(mz) > threshold, None, None

# ─── Relatório de outliers ─────────────────────────────────────────────────────
print("=" * 65)
print("RELATÓRIO DE OUTLIERS — Emissões de GEE por Setor (Portugal)")
print("=" * 65)

pollutants = ['GHG', 'CO2', 'CH4', 'N2O']   # excluímos CH4_CO2E (redundante com CH4)
sectors    = ['CRF1', 'CRF1A', 'CRF1A1', 'TOTX4_MEMO', 'TOTXMEMO']

results = []
for pol in pollutants:
    for sec in sectors:
        subset = df[(df['airpol'] == pol) & (df['src_crf'] == sec)].copy()
        if len(subset) < 5:
            continue
        mask_iqr, lower, upper = iqr_outliers(subset['OBS_VALUE'])
        mask_mz, _, _           = modified_zscore_outliers(subset['OBS_VALUE'])
        n_iqr = mask_iqr.sum()
        n_mz  = mask_mz.sum()
        if n_iqr > 0 or n_mz > 0:
            print(f"\n▸ {POLLUTANT_LABELS.get(pol, pol)} | {SECTOR_LABELS.get(sec, sec)}")
            print(f"  IQR: {n_iqr} outlier(s) | Mod. Z-Score: {n_mz} outlier(s)")
            if n_iqr > 0:
                out_rows = subset[mask_iqr][['TIME_PERIOD', 'OBS_VALUE']]
                for _, r in out_rows.iterrows():
                    print(f"  → Ano {int(r['TIME_PERIOD'])}: {r['OBS_VALUE']:.2f}")
        results.append({'pol': pol, 'sec': sec, 'subset': subset,
                        'mask_iqr': mask_iqr, 'lower': lower, 'upper': upper})

# ─── Visualização ─────────────────────────────────────────────────────────────
# Outliers IQR — GHG por setor
fig2, axes2 = plt.subplots(1, len(sectors), figsize=(18, 5), sharey=False)
fig2.suptitle('Deteção de Outliers (IQR) — GHG por Setor — Portugal', fontsize=12, fontweight='bold')

for ax, sec in zip(axes2, sectors):
    subset = df[(df['airpol'] == 'GHG') & (df['src_crf'] == sec)].sort_values('TIME_PERIOD').reset_index(drop=True)
    if subset.empty:
        ax.set_visible(False)
        continue
    mask_iqr, lower, upper = iqr_outliers(subset['OBS_VALUE'])
    x = subset['TIME_PERIOD']

    ax.scatter(x[~mask_iqr], subset['OBS_VALUE'][~mask_iqr],
               color='steelblue', s=30, alpha=0.7, label='Normal')
    if mask_iqr.sum() > 0:
        ax.scatter(x[mask_iqr], subset['OBS_VALUE'][mask_iqr],
                   color='red', s=60, zorder=5, label=f'Outlier ({mask_iqr.sum()})')
    ax.axhline(lower, color='orange', linestyle='--', linewidth=1, label=f'Inf. ({lower:.0f})')
    ax.axhline(upper, color='orange', linestyle='--', linewidth=1, label=f'Sup. ({upper:.0f})')
    ax.set_title(SECTOR_LABELS.get(sec, sec), fontsize=8)
    ax.set_xlabel('Ano', fontsize=8)
    ax.tick_params(axis='x', rotation=45, labelsize=7)
    ax.tick_params(axis='y', labelsize=7)
    ax.legend(fontsize=6)

plt.tight_layout()
plt.savefig('emissoes_outliers.png', dpi=150, bbox_inches='tight')
print("Gráfico 2 guardado: emissoes_outliers.png")