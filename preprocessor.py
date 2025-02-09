import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user messages':messages,'message_date':dates})
    df['message_date'] = pd.to_datetime (df['message_date'], format='%d/%m/%y, %H:%M - ')
    users=[]
    messages=[]
    for msg in df['user messages']:
        entry = re.split(r'(.*?):\s', msg, maxsplit=1)
        
        if len(entry) > 2:
            users.append(entry[1])  # Extract the user's name
            messages.append(entry[2])  # Extract the message
        else:
            users.append('grp notification')
            messages.append(entry[0])
    df['users']=users
    df['messages']=messages
    df.drop(columns=['user messages'],inplace=True)
    df['date']=df['message_date'].dt.day
    df['only_date'] = df['message_date'].dt.date
    df['year']=df['message_date'].dt.year.astype(str)
    df['month_num'] = df['message_date'].dt.month
    df['month']=df['message_date'].dt.month_name()
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour']=df['message_date'].dt.hour
    df['minute']=df['message_date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df
