from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji



extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        num_messages = df.shape[0]
        words_list = []
        for message in df['message']:
            words_list.extend(message.split())
        total_words = len(words_list)
        num_media= 0
        for message in df['message']:
            if "<Media omitted>" in message:
                num_media += 1  
        urls  =0
        for message in df['message']:
            if extractor.find_urls(message):
                urls += 1
        
    else:
        filtered_df = df[df['user_name'] == selected_user]
        num_messages = filtered_df.shape[0]
        words_list = []
        for message in filtered_df['message']:
            words_list.extend(message.split())
        total_words = len(words_list)
        num_media = 0
        for message in filtered_df['message']:
            if "<Media omitted>" in message:
                num_media += 1
        urls = 0
        for message in filtered_df['message']:
            if extractor.find_urls(message):
                urls += 1
        
    return num_messages, total_words, num_media, urls


def most_busy_users(df):
    x = df['user_name'].value_counts().head()
    percent_df = round((df['user_name'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'user_name':'name', 'count':'percent'}) 
    return x, percent_df


f = open("stopwords.txt", "r")
stopwords = f.read()

def generate_wordcloud(selected_user, df):
    wc = WordCloud(width=500, height=300, max_words=200, background_color='white')
    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)
    if selected_user == 'Overall':
        temp = df[df['user_name'] != 'system_notification']
        temp['message'] = temp['message'].apply(remove_stopwords)
        df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    else:
        filtered_df = df[df['user_name'] == selected_user]
        temp = filtered_df[filtered_df['user_name'] != 'system_notification']
        temp['message'] = temp['message'].apply(remove_stopwords)
        df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc



def most_common_words(selected_user, df):
    if selected_user == 'Overall':
        temp = df[df['user_name'] != 'system_notification']
        words = []
        for message in temp['message']:
            for word in message.lower().split():
                if word not in stopwords:
                    words.append(word)
        common_words_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])
        emojis = []
        for message in temp['message']:
            for char in message:
                if char in emoji.EMOJI_DATA.keys():
                    emojis.append(char)
        emoji_df = pd.DataFrame(Counter(emojis).most_common(20), columns=['emoji', 'count'])

    else:
        filtered_df = df[df['user_name'] == selected_user]
        temp = filtered_df[filtered_df['user_name'] != 'system_notification']
        words = []
        for message in temp['message']:
            for word in message.lower().split():
                if word not in stopwords:
                    words.append(word)
        common_words_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])
        emojis = []
        for message in temp['message']:
            for char in message:
                if char in emoji.EMOJI_DATA.keys():
                    emojis.append(char)
        emoji_df = pd.DataFrame(Counter(emojis).most_common(20), columns=['emoji', 'count'])
    
    return common_words_df, emoji_df


def create_timeline(selected_user,df):
    if selected_user == 'Overall':
        timeline = df.groupby(['year', 'month']).count()['message'].reset_index()
        time = []
        for i in range(timeline.shape[0]):
            time.append(timeline['month'][i] + "-" + timeline['year'][i])
        timeline['time'] = time
    
    else:
        filtered_df = df[df['user_name'] == selected_user]
        timeline = filtered_df.groupby(['year', 'month']).count()['message'].reset_index()
        time = []
        for i in range(timeline.shape[0]):
            time.append(timeline['month'][i] + "-" + timeline['year'][i])
        timeline['time'] = time
    
    return timeline

def week_activity(selected_user, df):
    if selected_user == 'Overall':
        week_activity = df['day_name'].value_counts().sort_index(key=lambda x: x.map({"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}))
    else:
        filtered_df = df[df['user_name'] == selected_user]
        week_activity = filtered_df['day_name'].value_counts().sort_index(key=lambda x: x.map({"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}))
    return week_activity

def month_activity(selected_user, df):
    if selected_user == 'Overall':
        month_activity = df['month'].value_counts().sort_index()
    else:
        filtered_df = df[df['user_name'] == selected_user]
        month_activity = filtered_df['month'].value_counts().sort_index()
    return month_activity


def activity_heatmap(selected_user, df):
    if selected_user == 'Overall':
        activity_table = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)   
    else:
        filtered_df = df[df['user_name'] == selected_user]
        activity_table = filtered_df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_table