import pandas as pd
import json
from extract_dataframe import extract_dataframe, extract_dataframe_daily, is_default_facebook_intervention, is_default_youtube_intervention, at_least_two_conditions, is_facebook, is_youtube, exclude_first_day, exclude_last_day

datafile = 'data_april1_4am.json'
datafile_base = datafile.replace('.json', '')
alldata = json.load(open(datafile))

def extract_to_file_with_filters(filename, filters=[], user_filters=[]):
  extract_dataframe(alldata, filters).to_csv(filename, index=False)

def extract_to_file_with_filters_day(filename, filters=[], user_filters=[]):
  extract_dataframe_daily(alldata, filters).to_csv(filename, index=False)

extract_to_file_with_filters(datafile_base + '.csv')
extract_to_file_with_filters(datafile_base + '_facebook_only.csv', is_facebook)
extract_to_file_with_filters(datafile_base + '_no_first_last.csv', [exclude_first_day, exclude_last_day])
extract_to_file_with_filters(datafile_base + '_facebook_only_default_interventions_only.csv', [is_facebook, is_default_facebook_intervention])
extract_to_file_with_filters(datafile_base + '_youtube_only.csv', is_youtube)
extract_to_file_with_filters(datafile_base + '_youtube_only_default_interventions_only.csv', [is_youtube, is_default_youtube_intervention])
extract_to_file_with_filters(datafile_base + '_facebook_only_default_interventions_only_both_conditions.csv', [is_facebook, is_default_facebook_intervention], [at_least_two_conditions])

extract_to_file_with_filters_day(datafile_base + '_days.csv', [], [])
extract_to_file_with_filters_day(datafile_base + '_facebook_only_days_only_both_conditions.csv', [is_facebook], [at_least_two_conditions])
