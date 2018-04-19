#!/usr/bin/env python3

from csv import DictReader
import pandas as pd

qualitative_data_file = 'qualitative_data_nofeedback_april18_3am.csv'
outputfile = 'qualitative_data_with_studies_april18_3am.csv'
study1_data_file = 'data_april3_1am_peruser.csv'
study2_data_file = 'exp2_april18_3am_withsessionlengths.csv'
study3_data_file = 'exp3_april16_1am.csv'

qualitative_data = [row for row in DictReader(open(qualitative_data_file))]
study1_data = [row for row in DictReader(open(study1_data_file))]
study2_data = [row for row in DictReader(open(study2_data_file))]
study3_data = [row for row in DictReader(open(study3_data_file))]

study1_userid_to_row = {}
for row in study1_data:
  userid = row['userid']
  study1_userid_to_row[userid] = row

study2_userid_to_row = {}
for row in study2_data:
  userid = row['userid']
  study2_userid_to_row[userid] = row

study3_userid_to_row = {}
for row in study3_data:
  userid = row['userid']
  study3_userid_to_row[userid] = row

userid_list_with_qualitative_data = []
userid_set_with_qualitative_data = set()
userid_to_last_qualitative_data = {}
for row in qualitative_data:
  userid = row['userid']
  if userid not in userid_set_with_qualitative_data:
    userid_set_with_qualitative_data.add(userid)
    userid_list_with_qualitative_data.append(userid)
  userid_to_last_qualitative_data[userid] = row

qualitative_data_last_for_each_user = []
for userid in userid_list_with_qualitative_data:
  row = userid_to_last_qualitative_data[userid]
  qualitative_data_last_for_each_user.append(row)

output = []
for row in qualitative_data_last_for_each_user:
  userid = row['userid']
  study = 'none'
  condition = 'none'
  study1condition = 'none'
  study1firstcondition = 'none'
  study2condition = 'none'
  study3condition = 'none'
  study3did_user_change_interventions = 'none'
  if userid in study1_userid_to_row:
    study = 'study1'
    st = study1_userid_to_row[userid]
    study1condition = st['last_condition_for_user']
    study1firstcondition = st['first_condition_for_user']
    condition = study1condition
  elif userid in study2_userid_to_row:
    study = 'study2'
    st = study2_userid_to_row[userid]
    study2condition = st['condition']
    condition = study2condition
  elif userid in study3_userid_to_row:
    study = 'study3'
    st = study3_userid_to_row[userid]
    study3condition = st['condition']
    condition = study3condition
    study3did_user_change_interventions = st['did_user_change_interventions']
  row['study'] = study
  row['condition'] = condition
  row['study1firstcondition'] = study1firstcondition
  row['study1condition'] = study1condition
  row['study2condition'] = study2condition
  row['study3condition'] = study3condition
  row['study3did_user_change_interventions'] = study3did_user_change_interventions
  #del(row['feedback'])
  output.append(row)

pd.DataFrame(output).to_csv(outputfile, index=False)
