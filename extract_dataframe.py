import pandas as pd
from math import log

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

def extract_dataframe(alldata, filter_funcs=[]):
  if callable(filter_funcs):
    filter_funcs = [filter_funcs]
  rows = []
  for install_id,experiment_info_with_sessions in alldata.items():
    for experiment_info in experiment_info_with_sessions:
      for condition_info in experiment_info['condition_info_list']:
        condition = condition_info['condition']
        for day_info in condition_info['day_info_list']:
          total_time_on_day = 0
          for session_info in day_info['session_info_list']:
            domain = session_info['domain']
            userid = session_info['userid']
            time_spent = session_info['time_spent']
            timestamp = session_info['timestamp']
            intervention = session_info['intervention']
            #if domain != 'www.facebook.com':
            #  continue
            row = {
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
  return pd.DataFrame(rows)

def extract_dataframe_daily(alldata, filter_funcs=[]):
  if callable(filter_funcs):
    filter_funcs = [filter_funcs]
  rows = []
  for install_id,experiment_info_with_sessions in alldata.items():
    for experiment_info in experiment_info_with_sessions:
      for condition_info in experiment_info['condition_info_list']:
        condition = condition_info['condition']
        for day_info in condition_info['day_info_list']:
          total_time_on_day = 0
          for session_info in day_info['session_info_list']:
            domain = session_info['domain']
            userid = session_info['userid']
            time_spent = session_info['time_spent']
            timestamp = session_info['timestamp']
            intervention = session_info['intervention']
            #if domain != 'www.facebook.com':
            #  continue
            row = {
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
  return pd.DataFrame(rows)

