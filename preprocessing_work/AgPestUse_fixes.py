import pandas as pd # pip install pandas

lowEst_df = pd.read_csv("../bee_data/dataset_2/LowEstimate_AgPestUsebyCropGroup92to17_v2.txt",
                        sep="\t", header=0)
highEst_df = pd.read_csv("../bee_data/dataset_2/HighEstimate_AgPestUsebyCropGroup92to17_v2.txt",
                        sep="\t", header=0)


# Filtering out non-neonicotinoids:

# Using info from https://en.wikipedia.org/wiki/Neonicotinoid
neonicotinoids = ['acetamiprid', 'clothianidin', 'dinotefuran', 'imidacloprid',
 'nitenpyram', 'nithiazine', 'thiacloprid', 'thiamethoxam']

 # Index 0 for LowEst data, Index 1 for HighEst data
 # Checks which neonicotinoids are in the corresponding datasets
neonics_in_data = [[],[]]

neonics_in_data[0] = [i.upper() for i in neonicotinoids if i.upper() in lowEst_df['Compound'].unique()]
neonics_in_data[1] = [i.upper() for i in neonicotinoids if i.upper() in highEst_df['Compound'].unique()]

# Gets rid of rows that address pesticides other than neonicotinoids
lowEst_df_filtered = lowEst_df[lowEst_df['Compound'].isin(neonics_in_data[0])]
highEst_df_filtered = highEst_df[highEst_df['Compound'].isin(neonics_in_data[1])]

# Checking how lengths of datasets change after filtering out non-neonicotinoids
# print(len(lowEst_df))
# print(len(LowEst_df_filtered), '\n')

# print(len(highEst_df))
# print(len(highEst_df_filtered))


# Filtering out unnecessary columns:

# I checked if any units were used besides kg
# for i in LowEst_df_filtered['Units']:
#     if i != "kg":
#         print(i)
#         break

# for i in highEst_df_filtered['Units']:
#     if i != "kg":
#         print(i)
#         break


# Only kg units were used, so I dropped the units column
lowEst_df_filtered = lowEst_df_filtered.drop('Units', axis=1)
highEst_df_filtered = highEst_df_filtered.drop('Units', axis=1)

# State_FIPS_code is not needed since we have the State column
# lowEst_df_filtered = lowEst_df_filtered.drop('State_FIPS_code', axis=1)
# highEst_df_filtered = highEst_df_filtered.drop('State_FIPS_code', axis=1)


# Sorting by year:

lowEst_df_filtered.sort_values(by=['Year'], inplace=True)
highEst_df_filtered.sort_values(by=['Year'], inplace=True)

# RemovingNaN (replacing with -1 for now)

# print(lowEst_df_filtered.isna().sum())
# print(highEst_df_filtered.isna().sum())

lowEst_df_filtered.fillna(value=-1, inplace=True)
highEst_df_filtered.fillna(value=-1, inplace=True)


# Reset indices in datasets
lowEst_df_filtered.reset_index(drop=True, inplace=True)
highEst_df_filtered.reset_index(drop=True, inplace=True)


# Printing cleaned datasets
#print(lowEst_df_filtered.head)
#print(highEst_df_filtered.head)

# Saving cleaned data
lowEst_df_filtered.to_csv('../preprocessed_bee_data/LowEst_AgPestUse_clean.csv')
highEst_df_filtered.to_csv('../preprocessed_bee_data/highEst_AgPestUse_clean.csv')
