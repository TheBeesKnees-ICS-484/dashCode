import pandas as pd
from pathlib import Path

# I shortened "weighted tolerance index (WTI) compared with co-foraging species" to "relative WTI"
WTI = {"relative WTI": 
[3.30, 2.33, 2.00, 1.67, 1.50, 1.00, 0.33, -0.50, -0.67, -1.33] }

genuses = {"genus": ["Apis", "Xenoglossa", "Halictus", "Trachusa", "Ptilothrix", "Melissodes", "Bombus",
"Habropoda", "Svastra", "Peponapis"]}

WTI = dict(genuses, **WTI)

WTI_by_genus_df = pd.DataFrame(data = WTI)

#print(WTI_by_genus_df)

# Code help on exporting to csv from 
# https://stackoverflow.com/questions/47143836/pandas-dataframe-to-csv-raising-ioerror-no-such-file-or-directory
output_file = 'WTI_clean.csv'
output_dir = Path('../preprocessed_bee_data/')

output_dir.mkdir(parents=True, exist_ok=True)

WTI_by_genus_df.to_csv(output_dir / output_file, index=False)

