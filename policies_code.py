import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from collections import Counter

# ─── Carregar dados ────────────────────────────────────────────────────────────
df = pd.read_csv('policies_database.csv', sep=';', encoding='latin-1')
df = df.dropna(subset=['year']).reset_index(drop=True)
df['year'] = df['year'].astype(int)
df = df[(df['year'] >= 2004) & (df['year'] <= 2024)].reset_index(drop=True)

print(f"Total de políticas: {len(df)}")
print(f"Período: {df['year'].min()} – {df['year'].max()}")
print(f"\nStatus:\n{df['status'].value_counts()}")

# ─── Funções auxiliares ────────────────────────────────────────────────────────
def extract_names(text):
    if pd.isna(text) or str(text).strip() == '[]':
        return []
    return re.findall(r'"([^"]+)"', str(text))

def extract_topic(text):
    """Extrai o campo 'topic' das tags (formato JSON dentro do CSV)"""
    if pd.isna(text) or str(text).strip() == '[]':
        return []
    return re.findall(r'"topic"\s*:\s*"([^"]+)"', str(text))

df['tech_list']  = df['technologies'].apply(extract_names)
df['tags_list']  = df['tags'].apply(extract_names)
df['topic_list'] = df['tags'].apply(extract_topic)

# ─── Visualização ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.suptitle('Políticas Energéticas de Portugal — IEA PAMS', fontsize=14, fontweight='bold')

COLORS = {
    'In force':  '#2E7D32',
    'Ended':     '#B0BEC5',
    'Announced': '#F9A825',
    'Achieved':  '#1565C0',
}

# ── 1. Políticas por ano (empilhado por status) ────────────────────────────────
ax1 = axes[0, 0]
status_year = df.groupby(['year', 'status']).size().unstack(fill_value=0)
status_year = status_year.reindex(columns=['In force', 'Announced', 'Ended'], fill_value=0)
bottom = pd.Series(0, index=status_year.index)
for status, color in [('In force','#2E7D32'), ('Announced','#F9A825'), ('Ended','#B0BEC5')]:
    if status in status_year.columns:
        ax1.bar(status_year.index, status_year[status], bottom=bottom,
                label=status, color=color, alpha=0.85, width=0.8)
        bottom += status_year[status]
ax1.set_title('Novas Políticas por Ano')
ax1.set_xlabel('Ano')
ax1.set_ylabel('Nº de Políticas')
ax1.legend(fontsize=8)
ax1.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax1.tick_params(axis='x', rotation=45)

# ── 2. Políticas ativas vs terminadas (pizza) ──────────────────────────────────
ax2 = axes[0, 1]
status_counts = df[df['status'] != 'Achieved']['status'].value_counts()
colors_pie = [COLORS.get(s, '#90A4AE') for s in status_counts.index]
wedges, texts, autotexts = ax2.pie(
    status_counts,
    labels=status_counts.index,
    colors=colors_pie,
    autopct='%1.1f%%',
    startangle=140,
    pctdistance=0.8,
)
for t in autotexts:
    t.set_fontsize(9)
ax2.set_title('Distribuição por Estado')

# ── 3. Top 10 tecnologias ──────────────────────────────────────────────────────
ax3 = axes[1, 0]
all_tech = [t for sublist in df['tech_list'] for t in sublist]
top_tech = Counter(all_tech).most_common(10)
labels_t, values_t = zip(*top_tech)
# Encurtar labels longas
bars = ax3.barh(labels_t[::-1], values_t[::-1], color='steelblue', alpha=0.8)
ax3.set_title('Top 10 Tecnologias Abrangidas', fontsize=10)
ax3.set_xlabel('Nº de Políticas')
ax3.tick_params(axis='y', labelsize=8)
for bar, val in zip(bars, values_t[::-1]):
    ax3.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
             str(val), va='center', fontsize=8)

# ── 4. Evolução cumulativa de políticas ativas ─────────────────────────────────
ax4 = axes[1, 1]
in_force = df[df['status'] == 'In force'].groupby('year').size()
cumulative = in_force.cumsum()
ax4.fill_between(cumulative.index, cumulative.values, alpha=0.3, color='#2E7D32')
ax4.plot(cumulative.index, cumulative.values, color='#2E7D32', linewidth=2, marker='o', markersize=4)
ax4.set_title('Políticas "In Force" — Acumulado')
ax4.set_xlabel('Ano')
ax4.set_ylabel('Nº Acumulado')
ax4.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('politicas_analise.png', dpi=150, bbox_inches='tight')
plt.show()
print("Gráfico guardado em politicas_analise.png")