#!/usr/bin/env python3

import numpy as np
import json

#datafile = 'data_april3_1am.json'
datafile = 'exp3_data.json'
alldata = json.load(open(datafile))

def get_firstlast_info(experiment_info_with_sessions):
  first_timestamp = None
  last_timestamp = None
  first_localepoch = None
  last_localepoch = None
  for experiment_info in experiment_info_with_sessions:
    for condition_info in experiment_info['condition_info_list']:
      for day_info in condition_info['day_info_list']:
        for session_info in day_info['session_info_list']:
          timestamp = session_info['timestamp']
          localepoch = session_info['localepoch']
          if first_localepoch == None:
            first_localepoch = localepoch
          else:
            first_localepoch = min(first_localepoch, localepoch)
          if last_localepoch == None:
            last_localepoch = localepoch
          else:
            last_localepoch = max(last_localepoch, localepoch)
          if first_timestamp == None:
            first_timestamp = timestamp
          else:
            first_timestamp = min(first_timestamp, timestamp)
          if last_timestamp == None:
            last_timestamp = timestamp
          else:
            last_timestamp = max(last_timestamp, timestamp)
  return {
    'first_timestamp': first_timestamp,
    'last_timestamp': last_timestamp,
    'first_localepoch': first_localepoch,
    'last_localepoch': last_localepoch,
  }

num_sessions_per_day = []
num_domains_per_user = []
fraction_days_per_user = []
num_sessions_per_day_avgpp = []
num_domains_per_user_avgpp = []
fraction_days_per_user_avgpp = []
for install_id,day_info_list in alldata.items():
  all_domains = set()
  num_sessions_today = 0
  all_localepochs = [x['localepoch'] for x in day_info_list]
  if len(all_localepochs) == 0:
    continue
  first_localepoch = min(all_localepochs)
  last_localepoch = max(all_localepochs)
  total_days = last_localepoch - first_localepoch
  if total_days == 0:
    continue
  days_seen_an_intervention = set()
  for session_info in day_info_list:
    localepoch = session_info['localepoch']
  num_sessions_within_today = []
  for session_info in day_info_list:
    print(session_info)
    num_sessions_today += 1
    domain = session_info['domain']
    all_domains.add(domain)
    localepoch = session_info['localepoch']
    if first_localepoch <= localepoch <= last_localepoch:
      days_seen_an_intervention.add(localepoch)
  if num_sessions_today > 0:
    num_sessions_per_day.append(num_sessions_today)
    num_sessions_within_today.append(num_sessions_today)
    if len(all_domains) > 0:
      num_domains_per_user.append(len(all_domains))
    if len(days_seen_an_intervention) > 0:
      if len(days_seen_an_intervention) > total_days:
        print(days_seen_an_intervention)
        print(first_localepoch)
        print(last_localepoch)
      fraction_days_per_user.append(len(days_seen_an_intervention) / (total_days + 1))
  break
  num_sessions_per_day_avgpp.append(np.mean(num_sessions_within_today))
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

print('num sessions per day avgpp')
print('num_sessions_per_day')
print(len(num_sessions_per_day))
print(len(num_sessions_per_day_avgpp))
print(np.mean(num_sessions_per_day_avgpp))
#print(np.std(num_sessions_per_day))
print(np.mean(num_domains_per_user))
#print(np.std(num_domains_per_user))
print(np.mean(fraction_days_per_user))
#print(np.std(fraction_days_per_user))
