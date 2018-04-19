import pandas as pd
from math import log, floor
from collections import Counter
import moment

def is_facebook(x):
  return x['domain'] == 'www.facebook.com'

def is_youtube(x):
  return x['domain'] == 'www.youtube.com'

default_facebook_interventions = [
  'facebook/feed_injection_timer',
  'facebook/remove_news_feed',
  'facebook/remove_comments',
  'facebook/toast_notifications',
  'facebook/show_timer_banner',
]

default_youtube_interventions = [
  'youtube/remove_sidebar_links',
  'youtube/prompt_before_watch',
  'youtube/remove_comment_section',
]

def is_default_facebook_intervention(x):
  return x['intervention'] in default_facebook_interventions

def is_default_youtube_intervention(x):
  return x['intervention'] in default_youtube_interventions

def at_least_two_conditions(experiment_info_with_sessions):
  if len(experiment_info_with_sessions) > 0 and len(experiment_info_with_sessions[0]['condition_info_list']) >= 2:
    return True
  return False

def to_unix_timestamp_day(timestamp):
  return round(timestamp / (24 * 3600 * 1000))

def exclude_first_day(x):
  return x['days_since_install'] > 0

def exclude_last_day(x):
  return x['days_until_last_day'] > 0

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

def get_did_user_experience_both_same_and_random(experiment_info_with_sessions):
  same_seen = False
  random_seen = False
  for experiment_info in experiment_info_with_sessions:
    for condition_info in experiment_info['condition_info_list']:
      condition = condition_info['condition']
      for day_info in condition_info['day_info_list']:
        for session_info in sorted(day_info['session_info_list'], key=lambda k: k['timestamp']):
          if condition == 'same':
            same_seen = True
          if condition == 'random':
            random_seen = True
  return same_seen and random_seen

def get_global_max_timestamp(alldata):
  max_timestamp = None
  for install_id,experiment_info_with_sessions in alldata.items():
    for experiment_info in experiment_info_with_sessions:
      for condition_info in experiment_info['condition_info_list']:
        for day_info in condition_info['day_info_list']:
          for session_info in sorted(day_info['session_info_list'], key=lambda k: k['timestamp']):
            timestamp = session_info['timestamp']
            if max_timestamp == None:
              max_timestamp = timestamp
            max_timestamp = max(max_timestamp, timestamp)
  return max_timestamp

def get_domain_to_num_samples(session_info_list):
  output = Counter()
  for session_info in session_info_list:
    domain = session_info['domain']
    output[domain] += 1
  return dict(output)

def get_domain_to_total_time_spent(session_info_list):
  output = Counter()
  for session_info in session_info_list:
    domain = session_info['domain']
    time_spent = session_info['time_spent']
    output[domain] += time_spent
  return dict(output)

def get_domain_to_last_timestamp(session_info_list):
  output = Counter()
  for session_info in session_info_list:
    domain = session_info['domain']
    timestamp = session_info['timestamp']
    output[domain] = max(output[domain], timestamp)
  return dict(output)

def extract_dataframe(alldata, filter_funcs=[], user_filter_funcs=[]):
  if callable(filter_funcs):
    filter_funcs = [filter_funcs]
  rows = []
  max_timestamp = get_global_max_timestamp(alldata)
  for install_id,experiment_info_with_sessions in alldata.items():
    accept_user = True
    for user_filter_func in user_filter_funcs:
      if not user_filter_func(experiment_info_with_sessions):
        accept_user = False
    if not accept_user:
      continue
    first_condition_for_user = None
    for experiment_info in experiment_info_with_sessions:
      for condition_info in experiment_info['condition_info_list']:
        condition = condition_info['condition']
        if first_condition_for_user == None:
          first_condition_for_user = condition
    first_conditionduration_for_user = None
    for experiment_info in experiment_info_with_sessions:
      for condition_info in experiment_info['condition_info_list']:
        conditionduration = condition_info['conditionduration']
        if first_conditionduration_for_user == None:
          first_conditionduration_for_user = conditionduration
    intervention_to_num_impressions = {}
    intervention_to_num_days_seen_at_least_once = {}
    #epoch = day_info['epoch']
    #if install_id not in install_id_to_first_epoch:
    #  install_id_to_first_epoch[install_id] = 0
    #else:
    #  install_id_to_first_epoch[install_id] = min(install_id_to_first_epoch[install_id], epoch)
    firstlast_info = get_firstlast_info(experiment_info_with_sessions)
    first_timestamp = firstlast_info['first_timestamp']
    last_timestamp = firstlast_info['last_timestamp']
    first_localepoch = firstlast_info['first_localepoch']
    last_localepoch = firstlast_info['last_localepoch']
    for experiment_info in experiment_info_with_sessions:
      for condition_info in experiment_info['condition_info_list']:
        condition = condition_info['condition']
        conditionduration = condition_info['conditionduration']
        for day_info in condition_info['day_info_list']:
          #is_day_with_just_one_sample = 0
          #if len(day_info['session_info_list']) < 2:
          #  is_day_with_just_one_sample = 1
          domain_to_num_samples = get_domain_to_num_samples(day_info['session_info_list'])
          intervention_to_num_impressions_today = {}
          intervention_to_seen_today_at_least_once = {}
          for session_info in sorted(day_info['session_info_list'], key=lambda k: k['timestamp']):
            domain = session_info['domain']
            userid = session_info['userid']
            time_spent = session_info['time_spent']
            timestamp = session_info['timestamp']
            intervention = session_info['intervention']
            if intervention not in intervention_to_num_impressions:
              intervention_to_num_impressions[intervention] = 0
            else:
              intervention_to_num_impressions[intervention] += 1
            if intervention not in intervention_to_num_impressions_today:
              intervention_to_num_impressions_today[intervention] = 0
            else:
              intervention_to_num_impressions_today[intervention] += 1
            if intervention not in intervention_to_seen_today_at_least_once:
              intervention_to_seen_today_at_least_once[intervention] = True
            num_days_intervention_seen_at_least_once = 0
            if intervention in intervention_to_num_days_seen_at_least_once:
              num_days_intervention_seen_at_least_once = intervention_to_num_days_seen_at_least_once[intervention]
            #if domain != 'www.facebook.com':
            #  continue
            timestamp = session_info['timestamp']
            is_last_intervention_for_user = timestamp == last_timestamp
            attritioned = False
            if is_last_intervention_for_user:
              if (moment.unix(max_timestamp) - moment.unix(last_timestamp)).days > 2:
                attritioned = True
            days_since_install = round((timestamp - first_timestamp) / (24*3600*1000))
            days_until_last_day = floor((last_timestamp - timestamp) / (24*3600*1000))
            localepoch = session_info['localepoch']
            days_since_install = localepoch - first_localepoch
            days_until_last_day = last_localepoch - localepoch
            #print(days_until_last_day)
            is_first_visit_of_day = intervention_to_num_impressions_today[intervention] == 0
            row = {
              'first_condition_for_user': first_condition_for_user,
              'first_conditionduration_for_user': first_conditionduration_for_user,
              'attritioned': int(attritioned),
              'conditionduration': conditionduration,
              'days_since_install': days_since_install,
              'days_until_last_day': days_until_last_day,
              'num_days_intervention_seen_at_least_once': num_days_intervention_seen_at_least_once,
              'timestamp': timestamp,
              'is_day_with_just_one_sample': int(domain_to_num_samples[domain] == 1),
              'impression_idx': intervention_to_num_impressions[intervention],
              'is_first_visit_of_day': int(is_first_visit_of_day),
              'impression_idx_within_day': intervention_to_num_impressions_today[intervention],
              'log_time_spent': log(time_spent),
              'time_spent': time_spent,
              'install_id': install_id,
              'userid': userid,
              'condition': condition,
              'intervention': intervention,
              'domain': domain,
            }
            accept = True
            for filter_func in filter_funcs:
              if not filter_func(row):
                accept = False
            if accept:
              rows.append(row)
          for intervention in intervention_to_seen_today_at_least_once.keys():
            if intervention not in intervention_to_num_days_seen_at_least_once:
              intervention_to_num_days_seen_at_least_once[intervention] = 1
            else:
              intervention_to_num_days_seen_at_least_once[intervention] += 1
  return pd.DataFrame(rows)

def extract_dataframe_daily(alldata, day_filter_funcs=[], user_filter_funcs=[]):
  if callable(day_filter_funcs):
    day_filter_funcs = [filter_funcs]
  rows = []
  install_id_to_first_condition = {}
  max_timestamp = get_global_max_timestamp(alldata)
  for install_id,experiment_info_with_sessions in alldata.items():
    accept_user = True
    if len(experiment_info_with_sessions) == 0:
      continue
    for user_filter_func in user_filter_funcs:
      if not user_filter_func(experiment_info_with_sessions):
        accept_user = False
    if not accept_user:
      continue
    first_condition_for_user = None
    for experiment_info in experiment_info_with_sessions:
      for condition_info in experiment_info['condition_info_list']:
        condition = condition_info['condition']
        if first_condition_for_user == None:
          first_condition_for_user = condition
    first_conditionduration_for_user = None
    for experiment_info in experiment_info_with_sessions:
      for condition_info in experiment_info['condition_info_list']:
        conditionduration = condition_info['conditionduration']
        if first_conditionduration_for_user == None:
          first_conditionduration_for_user = conditionduration
    install_id_to_first_condition[install_id] = first_condition_for_user
    firstlast_info = get_firstlast_info(experiment_info_with_sessions)
    first_localepoch = firstlast_info['first_localepoch']
    last_localepoch = firstlast_info['last_localepoch']
    last_timestamp = firstlast_info['last_timestamp']
    user_saw_both_same_and_random = get_did_user_experience_both_same_and_random(experiment_info_with_sessions)
    for experiment_info in experiment_info_with_sessions:
      num_days_in_same_condition = 0
      num_days_in_same_condition_and_saw_intervention = 0
      intervention_to_num_days_seen_at_least_once = Counter()
      for condition_info in experiment_info['condition_info_list']:
        condition = condition_info['condition']
        conditionduration = condition_info['conditionduration']
        for day_info in condition_info['day_info_list']:
          domain_to_num_samples = get_domain_to_num_samples(day_info['session_info_list'])
          #is_day_with_just_one_sample = 0
          #if len(day_info['session_info_list']) < 2:
          #  is_day_with_just_one_sample = 1
          domain_to_total_time_spent = get_domain_to_total_time_spent(day_info['session_info_list'])
          domain_to_last_timestamp = get_domain_to_last_timestamp(day_info['session_info_list'])
          day_intervention = 'random'
          domain_to_num_impressions_on_day = {}
          last_timestamp_on_day = None
          days_since_install = None
          days_until_last_day = None
          domain_to_last_timestamp = {}
          saw_intervention_today_same = False
          interventions_seen_today = set()
          for session_info in sorted(day_info['session_info_list'], key=lambda k: k['timestamp']):
            domain = session_info['domain']
            if domain not in domain_to_num_impressions_on_day:
              domain_to_num_impressions_on_day[domain] = 0
            else:
              domain_to_num_impressions_on_day[domain] += 1
            userid = session_info['userid']
            time_spent = session_info['time_spent']
            timestamp = session_info['timestamp']
            if domain not in domain_to_last_timestamp:
              domain_to_last_timestamp[domain] = timestamp
            else:
              domain_to_last_timestamp[domain] = max(timestamp, domain_to_last_timestamp[domain])
            if last_timestamp_on_day == None:
              last_timestamp_on_day = timestamp
            last_timestamp_on_day = max(last_timestamp_on_day, timestamp)
            intervention = session_info['intervention']
            interventions_seen_today.add(intervention)
            if condition == 'same':
              saw_intervention_today_same = True
              day_intervention = intervention
            localepoch = session_info['localepoch']
            days_since_install = localepoch - first_localepoch
            days_until_last_day = last_localepoch - localepoch
            #if domain != 'www.facebook.com':
            #  continue
          if len(day_info['session_info_list']) == 0:
            continue
          is_last_day = int(last_timestamp_on_day == last_timestamp)
          domain_to_attritioned = {}
          if is_last_day:
            for domain,last_timestamp_for_domain in domain_to_last_timestamp.items():
              if last_timestamp == last_timestamp_for_domain: # user attritioned on this domain
                days_until_final_impression = (moment.unix(max_timestamp) - moment.unix(last_timestamp)).days
                domain_to_attritioned[domain] = days_until_final_impression > 2
          attritioned_today = 0
          if len(day_info['session_info_list']) > 0 and is_last_day:
            if (moment.unix(max_timestamp) - moment.unix(last_timestamp)).days > 2:
              attritioned_today = 1
          for domain,total_time_spent in domain_to_total_time_spent.items():
            attritioned = 0
            if domain in domain_to_attritioned:
              attritioned = int(domain_to_attritioned[domain])
            row = {
              'conditionduration': conditionduration,
              'days_since_install': days_since_install,
              'days_until_last_day': days_until_last_day,
              'user_saw_both_same_and_random': int(user_saw_both_same_and_random),
              'num_visits_to_domain_today': domain_to_num_samples[domain],
              'is_day_with_just_one_sample': int(domain_to_num_samples[domain] == 1),
              'attritioned': attritioned,
              'attritioned_today': attritioned_today,
              'is_last_day': is_last_day,
              'first_condition_for_user': first_condition_for_user,
              'first_conditionduration_for_user': first_conditionduration_for_user,
              'intervention': day_intervention,
              'num_impressions_on_day': domain_to_num_impressions_on_day[domain],
              'log_time_spent': log(total_time_spent),
              'time_spent': total_time_spent,
              'install_id': install_id,
              'userid': userid,
              'condition': condition,
              'domain': domain,
              'num_days_in_same_condition': num_days_in_same_condition,
              'num_days_in_same_condition_and_saw_intervention': num_days_in_same_condition_and_saw_intervention,
            }
            row['num_days_saw_intervention_for_same_intervention'] = 0
            if condition == 'same':
              row['num_days_saw_intervention_for_same_intervention'] = intervention_to_num_days_seen_at_least_once[day_intervention]
            accept = True
            for day_filter_func in day_filter_funcs:
              if not day_filter_func(row):
                accept = False
            if accept:
              rows.append(row)
          for intervention in interventions_seen_today:
            intervention_to_num_days_seen_at_least_once[intervention] += 1
          if condition == 'same':
            num_days_in_same_condition += 1
            if saw_intervention_today_same:
              num_days_in_same_condition_and_saw_intervention += 1
  print(Counter(install_id_to_first_condition.values()))
  return pd.DataFrame(rows)

def extract_dataframe_peruser(alldata):
  rows = []
  install_id_to_first_condition = {}
  max_timestamp = get_global_max_timestamp(alldata)
  for install_id,experiment_info_with_sessions in alldata.items():
    userid = ''
    last_condition_for_user = ''
    firstlast_info = get_firstlast_info(experiment_info_with_sessions)
    first_localepoch = firstlast_info['first_localepoch']
    last_localepoch = firstlast_info['last_localepoch']
    first_timestamp = firstlast_info['first_timestamp']
    last_timestamp = firstlast_info['last_timestamp']
    if last_timestamp == None or first_timestamp == None:
      continue
    #days_kept_installed = (moment.unix(last_timestamp) - moment.unix(first_timestamp)).days
    days_kept_installed = last_localepoch - first_localepoch
    attritioned = (moment.unix(max_timestamp) - moment.unix(last_timestamp)).days > 2
    first_condition_for_user = None
    first_conditionduration_for_user = None
    for experiment_info in experiment_info_with_sessions:
      for condition_info in experiment_info['condition_info_list']:
        condition = condition_info['condition']
        conditionduration = condition_info['conditionduration']
        if first_condition_for_user == None:
          first_condition_for_user = condition
        if first_conditionduration_for_user == None:
          first_conditionduration_for_user = conditionduration
        for day_info in condition_info['day_info_list']:
          for session_info in sorted(day_info['session_info_list'], key=lambda k: k['timestamp']):
            last_condition_for_user = condition
            userid = session_info['userid']
            domain = session_info['domain']
    if first_condition_for_user == None or first_conditionduration_for_user == None:
      continue
    completed_first_condition = days_kept_installed >= first_conditionduration_for_user
    attritioned_during_first_condition = (not completed_first_condition) and attritioned
    rows.append({
      'userid': userid,
      'install_id': install_id,
      'last_condition_for_user': last_condition_for_user,
      'attritioned': int(attritioned),
      'days_kept_installed': days_kept_installed,
      'attritioned_during_first_condition': int(attritioned_during_first_condition),
      'completed_first_condition': int(completed_first_condition),
      'first_condition_for_user': first_condition_for_user,
      'first_conditionduration_for_user': first_conditionduration_for_user,
    })
  return pd.DataFrame(rows)
