import pandas as pd
import json
from extract_dataframe import extract_dataframe

datafile = 'data_march28_2am.json'
alldata = json.load(open(datafile))
data = extract_dataframe(alldata)
data.to_csv(datafile.replace('.json', '.csv'), index=False)
