import pandas as pd
import numpy as np
import os

df = pd.read_csv('LowEst_AgPestUse_clean.csv')
df = df.fillna(0)
states = df['State'].unique()
print(df.columns)
new_cols = ['State', 'Year', 'Corn', 'Soybeans', 'Wheat', 'Cotton', 'Vegetables_and_fruit', 'Rice',
            'Orchards_and_grapes', 'Alfalfa', 'Pasture_and_hay', 'Other_crops', 'All_Crops']


new_df = pd.DataFrame(columns=new_cols)
for state in states:
    state_df = df.loc[df['State'] == state].copy()
    years = state_df['Year'].unique()
    for year in years:
        row_dict = {}
        state_year_df = state_df.loc[state_df['Year'] == year]
        row_dict['State'] = state
        row_dict['Year'] = year
        for col in new_cols[2:]:
            row_dict[col] = state_year_df[col].sum()
        new_df = new_df.append(row_dict, ignore_index=True)

new_df.to_csv('LowEst_AgPestUse_Yearly_Combined.csv', index=False)