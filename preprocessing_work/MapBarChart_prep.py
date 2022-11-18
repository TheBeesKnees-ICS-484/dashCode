import pandas as pd

# Read in data

# Bee colony census data
bee_df = pd.read_csv("../bee_data/dataset_3/bee_colony_survey_data_by_state.csv")

# Neonic usage data
neonic_df = pd.read_csv("../preprocessed_bee_data/lowEst_AgPestUse_clean.csv")


# Get necessary columns

# Note: value is number of bees
bee_df = bee_df.filter(items=['year', 'value'])

# Note: Compound is neonicotinoid usage
# neonic_df = neonic_df.filter(items=['Year', 'Compound'])


# add a column for total neonic usage of all crops

crops = ['Corn', 'Soybeans','Wheat','Cotton','Vegetables_and_fruit','Rice','Orchards_and_grapes','Alfalfa','Pasture_and_hay','Other_crops']
neonics_crop_totals = []

neonic_df['Total Neonicotinoid Amount'] = neonic_df[crops].sum(axis=1)

# Get necessary columns for now

neonic_df = neonic_df.filter(items=['Year', 'Total Neonicotinoid Amount'])


# Restrict to time period 1992-2017

bee_df = bee_df[(1994 <= bee_df['year']) & (bee_df['year'] <= 2014)]

neonic_df = neonic_df.loc[(1994 <= neonic_df['Year']) & (neonic_df['Year'] <= 2014)]

# print(bee_df['year'].unique())
# print(neonic_df['Year'].unique())


# Sum up values and group by year

bee_df = bee_df.groupby(by='year', as_index=False).sum()

neonic_df = neonic_df.groupby(by='Year', as_index=False).sum() # Fix this, add up all crops for each row 


# print(neonic_df.head())

# Rename columns

bee_df.rename(columns={"year": "Year", "value": "Bee Count"}, inplace=True)

# neonic_df.rename(columns={'Year': 'Year', 'Compound': 'Neonicotinoid'}, inplace=True)

import numpy as np
r = np.corrcoef(neonic_df['Total Neonicotinoid Amount'], bee_df['Bee Count'])
print("Correlation matrix:", r)


# Normalize to range 0 and 1
bee_df['Bee Count'] = (bee_df['Bee Count']-bee_df['Bee Count'].min())/(bee_df['Bee Count'].max()-bee_df['Bee Count'].min())

neonic_df['Total Neonicotinoid Amount'] = (neonic_df['Total Neonicotinoid Amount']-neonic_df['Total Neonicotinoid Amount'].min())/(neonic_df['Total Neonicotinoid Amount'].max()-neonic_df['Total Neonicotinoid Amount'].min())

# Save preprocessed data

#lowEst_df_filtered.to_csv('../preprocessed_bee_data/LowEst_AgPestUse_clean.csv')
bee_df.to_csv('../preprocessed_bee_data/bee_summary_chart.csv')
neonic_df.to_csv('../preprocessed_bee_data/neonic_summary_chart.csv')




