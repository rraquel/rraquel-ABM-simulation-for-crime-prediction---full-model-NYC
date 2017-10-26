import pandas as pd
import numpy as np
import glob

glob.glob("../dev/batch results/combination tes/offender*.xlsx")

all_data = pd.DataFrame()
for f in glob.glob("../dev/batch results/combination tes/offender*.xlsx"):
    df = pd.read_excel(f)
    all_data = all_data.append(df,ignore_index=True)

    all_data.describe()

    all_data.head()