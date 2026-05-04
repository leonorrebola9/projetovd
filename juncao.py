import pandas as pd

EU27 = [
    'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
    'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece',
    'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg',
    'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania',
    'Slovakia', 'Slovenia', 'Spain', 'Sweden'
]

path = 'data/'

# 1. OWID CO2
co2 = pd.read_csv(path + 'owid-co2-data.csv', sep=';')
co2 = co2[co2['country'].isin(EU27) & co2['year'].between(2004, 2023)]
co2 = co2[['country', 'year', 'co2', 'co2_per_capita', 'primary_energy_consumption', 'population', 'gdp']]

# 2. Emissões anuais (GCP)
ann = pd.read_csv(path + 'annual-co2-emissions-per-country.csv', sep=';')
ann.rename(columns={'Entity': 'country', 'Year': 'year', 'Annual CO? emissions': 'annual_co2_tonnes'}, inplace=True)
ann = ann[ann['country'].isin(EU27) & ann['year'].between(2004, 2023)]
ann = ann[['country', 'year', 'annual_co2_tonnes']]

# 3. Balanços energéticos
bal = pd.read_csv(path + 'complete_energy_balances.csv', sep=';')
bal.rename(columns={'Geopolitical entity (reporting)': 'country', 'TIME_PERIOD': 'year', 'OBS_VALUE': 'value'}, inplace=True)
bal = bal[bal['country'].isin(EU27) & bal['year'].between(2004, 2023)]
bal_pivot = bal.pivot_table(index=['country', 'year'], columns='nrg_bal', values='value', aggfunc='sum').reset_index()
bal_pivot.columns.name = None
bal_pivot.rename(columns={
    'AFC': 'energy_available_final_consumption_ktoe',
    'FEC2020-2030': 'final_energy_consumption_ktoe',
    'GAE': 'gross_available_energy_ktoe',
    'NRGSUP': 'net_energy_supply_ktoe',
    'PEC2020-2030': 'primary_energy_consumption_ktoe'
}, inplace=True)

# 4. Quota de renováveis
ren = pd.read_csv(path + 'share_of_energy_from_renewable_sources.csv', sep=';', encoding='latin1')
ren.rename(columns={'geo': 'country', 'TIME_PERIOD': 'year', 'OBS_VALUE': 'renewables_share_pct'}, inplace=True)
ren = ren[ren['country'].isin(EU27) & ren['year'].between(2004, 2023)]
ren = ren[['country', 'year', 'renewables_share_pct']]

# 5. Investimento e patentes
inv = pd.read_csv(path + 'investimento_publico_e_privado.csv', sep=';', encoding='latin1')
inv['country'] = inv['country'].replace({'Czech Republic': 'Czechia'})
inv = inv[inv['country'].isin(EU27) & inv['year'].between(2004, 2023)]
for col in ['public_ri_investment', 'private_ri_investment', 'inventions']:
    inv[col] = inv[col].astype(str).str.replace(',', '.').astype(float)
inv_agg = inv.groupby(['country', 'year'])[['public_ri_investment', 'private_ri_investment', 'inventions']].sum().reset_index()
inv_agg.rename(columns={
    'public_ri_investment': 'public_rd_investment',
    'private_ri_investment': 'private_rd_investment',
    'inventions': 'clean_energy_patents'
}, inplace=True)

# 6. Merge
df = co2.merge(ann, on=['country', 'year'], how='outer')
df = df.merge(bal_pivot, on=['country', 'year'], how='outer')
df = df.merge(ren, on=['country', 'year'], how='outer')
df = df.merge(inv_agg, on=['country', 'year'], how='left')
df = df[df['country'].isin(EU27) & df['year'].between(2004, 2023)]
df = df.sort_values(['country', 'year']).reset_index(drop=True)

df.to_csv(path + 'eu27_energy_dataset_2004_2023.csv', index=False, sep=';')