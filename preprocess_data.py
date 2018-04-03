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

def print_num_users_in_data(filename):
  print('for data ' + filename)
  from csv import DictReader
  reader = DictReader(open(filename))
  install_ids = set()
  def get_conditionduration_to_install_ids(filter_func_list):
    conditionduration_to_install_ids = {
      '1': set(),
      '3': set(),
      '5': set(),
      '7': set(),
    }
    install_ids = set()
    for row in rows:
      accept_row = True
      for filter_func in filter_func_list:
        if not filter_func(row):
          accept_row = False
      if not accept_row:
        continue
      install_id = row['install_id']
      conditionduration = row['conditionduration']
      conditionduration_to_install_ids[conditionduration].add(install_id)
    print('total install ids: ' + str(len(install_ids)))
    for conditionduration,install_ids in conditionduration_to_install_ids.items():
      print(conditionduration + ' ' + str(len(install_ids)))
  rows = [row for row in reader]
  print('no filters')
  get_conditionduration_to_install_ids([])

  def exclude_is_day_with_just_one_sample(row):
    return int(row['is_day_with_just_one_sample']) == 0
  print('exclude is_day_with_just_one_sample')
  get_conditionduration_to_install_ids([exclude_is_day_with_just_one_sample])

  def days_since_install_greater_than_zero(row):
    return int(row['days_since_install']) > 0
  print('days_since_install_greater_than_zero')
  get_conditionduration_to_install_ids([exclude_is_day_with_just_one_sample, days_since_install_greater_than_zero])

print_num_users_in_data(datafile_base + '.csv')
print_num_users_in_data(datafile_base + '_days.csv')
