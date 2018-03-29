import pandas as pd
import json
from extract_dataframe import extract_dataframe

datafile = 'data_march28_2am.json'
datafile_base = datafile.replace('.json', '')
alldata = json.load(open(datafile))

def extract_to_file_with_filters(filename, filters=[]):
  extract_dataframe(alldata, filters).to_csv(filename, index=False)

extract_to_file_with_filters(datafile_base + '.csv')
extract_to_file_with_filters(datafile_base + '_facebook_only.csv', is_facebook)
extract_to_file_with_filters(datafile_base + '_facebook_only_default_interventions_only.csv', [is_facebook, is_default_facebook_intervention])
extract_to_file_with_filters(datafile_base + '_youtube_only.csv', is_youtube)
extract_to_file_with_filters(datafile_base + '_youtube_only_default_interventions_only.csv', [is_youtube, is_default_youtube_intervention])
