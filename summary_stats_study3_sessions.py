#!/usr/bin/env python3

import numpy as np
import json
from collections import Counter

#datafile = 'data_april3_1am.json'
#datafile = 'exp3_data_sessions.json'
datafile = 'exp2_data_sessions.json'
alldata = json.load(open(datafile))

userid_to_install_ids = {}
for userid,session_info_list in alldata.items():
  my_install_ids = set()
  for session_info in session_info_list:
    if 'install_id' in session_info:
      my_install_ids.add(session_info['install_id'])
  userid_to_install_ids[userid] = my_install_ids

num_sessions_per_day = []
num_domains_per_user = []
fraction_days_per_user = []
num_sessions_per_day_avgpp = []
num_domains_per_user_avgpp = []
fraction_days_per_user_avgpp = []
for userid,session_info_list in alldata.items():
  install_ids = userid_to_install_ids[userid]
  if len(install_ids) > 1:
    continue
  all_domains = set()
  num_sessions_today = 0
  all_localepochs = [x['localepoch'] for x in session_info_list]
  if len(all_localepochs) == 0:
    continue
  first_localepoch = min(all_localepochs)
  last_localepoch = max(all_localepochs)
  total_days = last_localepoch - first_localepoch
  if total_days == 0:
    continue
  if total_days < 2:
    continue
  days_seen_an_intervention = set()
  for session_info in session_info_list:
    localepoch = session_info['localepoch']
  localepoch_to_num_sessions = Counter()
  all_domains = set()
  if len(session_info_list) == 0:
    continue
  for session_info in session_info_list:
    localepoch = session_info['localepoch']
    localepoch_to_num_sessions[localepoch] += 1
    all_domains.add(session_info['domain'])
  if 'www.facebook.com' not in all_domains:
    continue
  avg_num_sessions = np.mean([x for x in localepoch_to_num_sessions.values()])
  fraction_days_seen = len([x for x in localepoch_to_num_sessions.keys()]) / (total_days + 1)
  num_domains = len(all_domains)
  num_sessions_per_day_avgpp.append(avg_num_sessions)
  num_domains_per_user_avgpp.append(num_domains)
  fraction_days_per_user_avgpp.append(fraction_days_seen)
  # firstlast_info = get_firstlast_info(experiment_info_with_sessions)
  # first_localepoch = firstlast_info['first_localepoch']
  # last_localepoch = firstlast_info['last_localepoch']
  # if first_localepoch == None or last_localepoch == None:
  #   continue
  # total_days = last_localepoch - first_localepoch
  # if total_days == 0:
  #   continue
  # days_seen_an_intervention = set()
  # all_domains = set()
  # for experiment_info in experiment_info_with_sessions:
  #   for condition_info in experiment_info['condition_info_list']:
  #     for day_info in condition_info['day_info_list']:
  #       num_sessions_today = 0
  #       for session_info in sorted(day_info['session_info_list'], key=lambda k: k['timestamp']):
  #         domain = session_info['domain']
  #         localepoch = session_info['localepoch']
  #         days_seen_an_intervention.add(localepoch)
  #         all_domains.add(domain)
  #         num_sessions_today += 1
  #       if num_sessions_today > 0:
  #         num_sessions_per_day.append(num_sessions_today)
  # num_domains = len(all_domains)
  # if num_domains > 0:
  #   num_domains_per_user.append(num_domains)
  # if len(days_seen_an_intervention) > 0:
  #   fraction_days_per_user.append(len(days_seen_an_intervention) / total_days)

#print('num sessions per day avgpp')
#print('num_sessions_per_day')
#print(len(num_sessions_per_day))
print(np.mean(num_sessions_per_day_avgpp))
#print(np.mean(num_sessions_per_day_avgpp))
#print(np.std(num_sessions_per_day))
print(np.mean(num_domains_per_user_avgpp))
#print(np.std(num_domains_per_user))
print(np.mean(fraction_days_per_user_avgpp))
#print(np.std(fraction_days_per_user))
