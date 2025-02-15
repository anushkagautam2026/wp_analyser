from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user,df):
    extractor=URLExtract()
    if(selected_user=='Overall'):
        links = []
        for message in df['messages']:
            links.extend(extractor.find_urls (message))
        
        return df.shape[0],df['messages'].str.split().str.len().sum(),df[df['messages']=='<Media omitted>\n'].shape[0],len(links)
    else:
        user_messages = df[df['users'] == selected_user]
        links = []
        for message in user_messages['messages']:
            links.extend(extractor.find_urls (message))
        return df['users'].value_counts()[selected_user],user_messages['messages'].str.split().str.len().sum(),user_messages[user_messages['messages']=='<Media omitted>\n'].shape[0],len(links)

def most_busy_users(df):
    x=df['users'].value_counts().head()
    df = round(df['users'].value_counts()/df.shape[0]*100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x,df
def create_wordcloud(selected_user,df):
    if(selected_user!='Overall'):
        df=df[df['users']==selected_user]
    wc=WordCloud(width=500,height=500,background_color='white',min_font_size=10)
    df_wc=wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user, df): 
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    if selected_user != 'Overall':
        df = df [df['users'] == selected_user]
        temp =df[df['users'] != 'group_notification']
        temp = temp[temp['messages'] != '<Media omitted>\n']
        
        for message in temp['messages']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)
    return_df=pd.DataFrame(Counter(words).most_common(20))
    return return_df
                    
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df [df['users'] == selected_user]
    emojis = [ ]
    for message in df ['messages']:
            emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame (Counter (emojis).most_common (len (Counter(emojis))))
    return emoji_df
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline
def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap
