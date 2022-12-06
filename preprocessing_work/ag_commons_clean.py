import pandas as pd
import numpy as np
import pathlib
import os
import matplotlib.pyplot as plt

# ICS484_Final/dashCode
path = pathlib.Path(__file__).parent.parent.resolve()

raw_data = pd.read_csv(os.path.join(path, 'bee_data/dataset_1', 'BEETOX RAW DATA AGCOMMONS 1.csv'))
raw_data = raw_data.drop(['Level of Sociality', 'Degree of floral specialization ', 'bee species', 'Date bee captured and installed in bioassay unit (Julian day)', 'bee sex',
               'bee longevity in bioassay (days)', 'days paralyzed', 'days active'], axis=1)
raw_data = raw_data.rename(columns={'Habitat floral host': 'floral_host', 'bee genus/species':'bee_genus_species',
                                    'Imidacloprid concentration (parts per billion)':'imidacloprid_ppb',
                                    '% of days bee is paralyzed': 'percent_days_paralyzed'})

raw_data['percent_days_paralyzed'] = raw_data['percent_days_paralyzed'].replace('.', '0')
raw_data = raw_data.astype({'floral_host': 'string', 'bee_genus_species': 'string',  'imidacloprid_ppb': 'int32', 'percent_days_paralyzed': 'int32'})
print(raw_data.dtypes)

raw_data.to_csv(os.path.join(path, 'preprocessed_bee_data', 'ag_commons_clean.csv'))