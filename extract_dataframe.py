import pandas as pd
from math import log

def extract_dataframe(alldata):
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
            rows.append({
              'log_time_spent': log(time_spent),
              'time_spent': time_spent,
              'install_id': install_id,
              'userid': userid,
              'condition': condition,
              'intervention': intervention,
              'domain': domain,
            })
  return pd.DataFrame(rows)
