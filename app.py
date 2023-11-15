import streamlit as st
import preprocessor, utils
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
      # To read file as bytes:
      bytes_data = uploaded_file.getvalue()
      data = bytes_data.decode("utf-8")
      df = preprocessor.preprocessor(data)

      userlist = df.user_name.unique().tolist()
      userlist.remove('system_notification')
      userlist.sort()
      userlist.insert(0, 'Overall')
      selected_user = st.sidebar.selectbox("Select User", userlist)

      if st.sidebar.button("Show Analysis"):
            num_messages, num_words, num_media, num_links = utils.fetch_stats(selected_user, df)
            st.title("Top Stats")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                  st.header("Total Messages")
                  st.title(num_messages)
            
            with col2:
                  st.header("Total Words")
                  st.title(num_words)

            with col3:
                  st.header("Media Shared")
                  st.title(num_media)

            with col4:
                  st.header("Links Shared")
                  st.title(num_links)

            if selected_user == 'Overall':
                  st.title("Busiest Users")
                  x, perecnt_df = utils.most_busy_users(df)
                  fig, ax = plt.subplots()
                  col1, col2 = st.columns(2)
                  with col1:
                        st.subheader("User Message plot")
                        ax.bar(x.index, x.values, color='red')
                        plt.xticks(rotation=45)
                        st.pyplot(fig)
                  
                  with col2:
                        st.subheader("Percentage of Messages")
                        st.dataframe(perecnt_df)

            st.title("WordCloud")
            wc = utils.generate_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(wc)
            st.pyplot(fig)

            most_common_df, common_emoji_df = utils.most_common_words(selected_user, df)
            
            fig, ax = plt.subplots()
            ax.barh(most_common_df['word'], most_common_df['count'])
            
            st.title("Most Common Words and Emojis")
            col1, col2 = st.columns(2)
            
            with col1:
                  st.subheader("Most Common Words")
                  st.pyplot(fig)
            
            with col2:
                  st.subheader("Most Common Emojis")
                  st.dataframe(common_emoji_df)

            timeline_df = utils.create_timeline(selected_user, df)
            
            fig, ax = plt.subplots(figsize=(16, 8))
            ax.plot(timeline_df['time'], timeline_df['message'])
            plt.xticks(rotation=90)
            st.title("Message Timeline")
            st.pyplot(fig, use_container_width=True)

            st.title("Activity Heatmap")
            col1, col2 = st.columns(2)

            with col1:
                  st.subheader("Weekly Activity")
                  weekly_activity = utils.week_activity(selected_user, df)
                  fig, ax = plt.subplots()
                  ax.bar(weekly_activity.index, weekly_activity.values)
                  plt.xticks(rotation=45)
                  st.pyplot(fig)
            
            with col2:
                  st.subheader("Monthly Activity")
                  monthly_activity = utils.month_activity(selected_user, df)
                  fig, ax = plt.subplots()
                  ax.bar(monthly_activity.index, monthly_activity.values, color='orange')
                  plt.xticks(rotation=45)
                  st.pyplot(fig)

            st.title("Activity Heatmap")
            activity_table = utils.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots(figsize=(16, 8))
            ax = sns.heatmap(activity_table)
            st.pyplot(fig)



                  
                  


                  


