import pandas as pd
import plotly.express as px

# 1. Läs in den sammanslagna tabellen (vi hoppar över MetaPhlAn-headers)
df = pd.read_csv('results/taxonomy/merged_abundance_table.txt', sep='\t', skiprows=1)

# 2. Filtrera för att bara se arter (s__) för att inte dubbelräkna familjer/släkten
df_species = df[df['clade_name'].str.contains('s__') & ~df['clade_name'].str.contains('t__')]

# 3. Snygga till namnen (ta bort k__Bacteria|p__... osv)
df_species['Species'] = df_species['clade_name'].apply(lambda x: x.split('s__')[-1])

# 4. Omvandla från "bred" till "lång" tabell (viktigt för Plotly)
df_melted = df_species.melt(id_vars=['Species'], 
                            value_vars=['SRR34737771_profile', 'SRR30914511_profile', 'SRR5169068_profile'],
                            var_name='Country', value_name='Relative_Abundance')

# Byt ut filnamn mot riktiga landsnamn
country_map = {
    'SRR34737771_profile': 'Slovakia',
    'SRR30914511_profile': 'UK',
    'SRR5169068_profile': 'Germany'
}
df_melted['Country'] = df_melted['Country'].map(country_map)

# 5. Skapa ett stapeldiagram för de 10 vanligaste arterna
top_species = df_melted.groupby('Species')['Relative_Abundance'].sum().nlargest(10).index
df_top = df_melted[df_melted['Species'].isin(top_species)]

fig = px.bar(df_top, x='Species', y='Relative_Abundance', color='Country',
             barmode='group', title='Top 10 Bacterial Species by Country',
             labels={'Relative_Abundance': 'Relativ abundans (%)'})

fig.show()
# För Streamlit använder du sen: st.plotly_chart(fig)
