import re
import pandas as pd


def split_datetime(datetime_string):
      date, time = datetime_string.split(',')
      day, month, year = date.split('/')
      hour, minute = time.split(':')
      if 'am' in minute:
            ampm = 'am'
            minute = minute.replace('am - ', '')
      else:
            ampm = 'pm'
            minute = minute.replace('pm - ', '')
      
      return day, month, year, hour, minute, ampm

def split_name(message_string):
      if ":" in message_string:
            name, message = message_string.split(':', 1)
      else:
            name = "system_notification"
            message = message_string
      
      return name, message


def preprocessor(data):
      pattern = '[0-9]+/[0-9]+/[0-9]+,\s[0-9]+:[0-9]+\s[A-Za-z]m\s-\s'
      messages = re.split(pattern, data)  
      messages.pop(0)
      dates = re.findall(pattern, data) 
      df = pd.DataFrame({'message_date': dates, 'user_message': messages})
      day_list = []
      month_list = []
      year_list = []
      hour_list = []
      minute_list = []
      ampm_list = []
      for datestring in df['message_date']:
            day, month, year, hour, minute,ampm = split_datetime(datestring)
            day_list.append(day)
            month_list.append(month)
            year_list.append(year)
            hour_list.append(hour)
            minute_list.append(minute)
            ampm_list.append(ampm)

      df['day'] = day_list
      df['month'] = month_list
      df['year'] = year_list
      df['hour'] = hour_list
      df['minute'] = minute_list
      df['ampm'] = ampm_list

      df['hour'] = df['hour'] + " " + df['ampm']

      df.drop(columns=['message_date', 'ampm'], inplace=True)
      name_list = []
      message_list = []
      for name_message in df['user_message']:
            name, message = split_name(name_message)
            name_list.append(name)
            message_list.append(message)

      df['user_name'] = name_list
      df['message'] = message_list

      df.drop(columns=['user_message'], inplace=True)
      df['date'] = df['day'] + "-" + df['month'] + "-" + df['year']
      df['date'] = pd.to_datetime(df['date'], format="%d-%m-%Y")
      df['day_name'] = df['date'].dt.day_name()
      period = []
      for hour in df['hour']:
            if '12' in hour:
                  period.append(str(hour) + " - " + "1 am/pm")
            else:
                  period.append(str(hour) + " - " + str(int(hour.split()[0]) + 1) + " " + hour.split()[1])
      df['period'] = period
      
      return df


