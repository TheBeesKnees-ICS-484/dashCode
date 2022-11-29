import pandas as pd
import numpy as np

# Read in data

# Bee colony census data
# State level
bee_state_df = pd.read_csv("../bee_data/dataset_3/bee_colony_survey_data_by_state.csv")
# County level
bee_county_df = pd.read_csv("../bee_data/dataset_3/bee_colony_census_data_by_county.csv")

# Neonic usage data
neonic_df = pd.read_csv("../preprocessed_bee_data/lowEst_AgPestUse_clean.csv")

# Get necessary columns

# Note: value is number of bees
bee_state_df = bee_state_df.filter(items=['year', 'value'])
bee_county_df = bee_county_df.filter(items=['year', 'value'])

# Note: Compound is neonicotinoid usage
# neonic_df = neonic_df.filter(items=['Year', 'Compound'])


# add a column for total neonic usage of all crops

crops = ['Corn', 'Soybeans','Wheat','Cotton','Vegetables_and_fruit','Rice','Orchards_and_grapes','Alfalfa','Pasture_and_hay','Other_crops']
neonics_crop_totals = []

neonic_df['Total Neonicotinoid Amount'] = neonic_df[crops].sum(axis=1)

# Get necessary columns for now

neonic_df = neonic_df.filter(items=['Year', 'Total Neonicotinoid Amount'])

# Drop rows with (D) for county level bee map
#bee_county_df = bee_county_df[bee_county_df['value'] != "(D)"]

bee_county_df['value'] = bee_county_df['value'].replace("(D)", np.nan)

bee_county_df['value'] = bee_county_df['value'].str.replace(",", "") # For numbers with commas ex 1,000
bee_county_df['value'] = pd.to_numeric(bee_county_df['value'])

bee_county_df['value'] = bee_county_df['value'].replace(np.nan, bee_county_df['value'].mean())

# Restrict to time period 1992-2017

bee_state_df = bee_state_df[(1994 <= bee_state_df['year']) & (bee_state_df['year'] <= 2017)]
bee_county_df = bee_county_df[(1994 <= bee_county_df['year']) & (bee_county_df['year'] <= 2017)]

neonic_df = neonic_df.loc[(1994 <= neonic_df['Year']) & (neonic_df['Year'] <= 2017)]

# print(bee_state_df['year'].unique())
# print(neonic_df['Year'].unique())


# Sum up values and group by year
# print(bee_state_df[bee_state_df['year'] == 2015].sum()) # checking when values explode

bee_state_df = bee_state_df.groupby(by='year', as_index=False).sum()
bee_county_df = bee_county_df.groupby(by='year', as_index=False).sum()

neonic_df = neonic_df.groupby(by='Year', as_index=False).sum() # Fix this, add up all crops for each row 

# print(neonic_df.head())

# Rename columns

bee_state_df.rename(columns={"year": "Year", "value": "Bee Count"}, inplace=True)
bee_county_df.rename(columns={"year": "Year", "value": "Bee Count"}, inplace=True)

# neonic_df.rename(columns={'Year': 'Year', 'Compound': 'Neonicotinoid'}, inplace=True)

# Normalize to range 0 and 1

bee_state_df_normal = bee_state_df.copy()
bee_county_df_normal = bee_county_df.copy()
neonic_df_normal = neonic_df.copy()

bee_state_df_normal['Bee Count'] = (bee_state_df['Bee Count']-bee_state_df['Bee Count'].min())/(bee_state_df['Bee Count'].max()-bee_state_df['Bee Count'].min())
bee_county_df_normal['Bee Count'] = (bee_county_df['Bee Count']-bee_county_df['Bee Count'].min())/(bee_county_df['Bee Count'].max()-bee_county_df['Bee Count'].min())

neonic_df_normal['Total Neonicotinoid Amount'] = (neonic_df['Total Neonicotinoid Amount']-neonic_df['Total Neonicotinoid Amount'].min())/(neonic_df['Total Neonicotinoid Amount'].max()-neonic_df['Total Neonicotinoid Amount'].min())

# Computing correlation matrix
r = np.corrcoef(neonic_df['Total Neonicotinoid Amount'], bee_state_df['Bee Count'])
print("Correlation matrix:", r)

# Save preprocessed data

#lowEst_df_filtered.to_csv('../preprocessed_bee_data/LowEst_AgPestUse_clean.csv')

# State level
bee_state_df.to_csv('../preprocessed_bee_data/bee_colony_data/state_level/bee_state_summary_chart.csv')
bee_state_df_normal.to_csv('../preprocessed_bee_data/bee_colony_data/state_level/bee_state_summary_chart_normalized.csv')
# County level
bee_county_df.to_csv('../preprocessed_bee_data/bee_colony_data/county_level/bee_county_summary_chart.csv')
bee_county_df_normal.to_csv('../preprocessed_bee_data/bee_colony_data/county_level/bee_county_summary_chart_normalized.csv')

neonic_df.to_csv('../preprocessed_bee_data/neonic_data/neonic_summary_chart.csv')
neonic_df_normal.to_csv('../preprocessed_bee_data/neonic_data/neonic_summary_chart_normalized.csv')




