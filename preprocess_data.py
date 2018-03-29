import pandas as pd
import json
from extract_dataframe import extract_dataframe

datafile = 'data_march28_2am.json'
datafile_base = datafile.replace('.json', '')
alldata = json.load(open(datafile))

def extract_to_file_with_filters(filename, filters=[]):
  extract_dataframe(alldata, filters).to_csv(filename, index=False)

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

extract_to_file_with_filters(datafile_base + '.csv')
extract_to_file_with_filters(datafile_base + '_facebook_only.csv', is_facebook)
extract_to_file_with_filters(datafile_base + '_facebook_only_default_interventions_only.csv', [is_facebook, is_default_facebook_intervention])
extract_to_file_with_filters(datafile_base + '_youtube_only.csv', is_youtube)
extract_to_file_with_filters(datafile_base + '_youtube_only_default_interventions_only.csv', [is_youtube, is_default_youtube_intervention])
