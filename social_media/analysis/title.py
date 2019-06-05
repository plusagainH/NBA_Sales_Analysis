import pickle
import pandas as pd
from datetime import datetime, timedelta, timezone


with open('team.pkl', 'rb') as f:
    team = pickle.load(f)
    
with open('schedule20122013.pkl', 'rb') as f: #<-change season here
    df_team_list = pickle.load(f)
    
def datetime_to_unix_timestamp(date):
    return int(date.timestamp())
for l in range(30):
    df_team_list[l]['game_unix_timestamp']=df_team_list[l]['gameDateEst']
    df_team_list[l]['game_unix_timestamp']=df_team_list[l]['game_unix_timestamp'].apply(datetime_to_unix_timestamp)
    df_team_list[l]['score']=None
    df_team_list[l]['num_comments']=None
    df_team_list[l]['score_norm']=None
    df_team_list[l]['num_comments_norm']=None
    df_team_list[l]['title']=None
#print(df_team_list[3]['score_norm'])

for k in range(30):    #30 team
    team_name=team[k][0]
    
    with open(team_name+'_post1213.pkl', 'rb') as f: #<-change season here
        post = pickle.load(f)
    
    df =pd.DataFrame(post)
    df2 = df 
    c=0
    d=0
    
    for i in range(len(df['title'])):
        title=df['title'][i].lower()
        time=int(df['created_utc'][i])
        if ('game thread' in title) and ('post game thread' not in title):
            if ('post-game thread' not in title) and ('@' not in title):
                c=title
                d=time
                
                distance=100000000
                temp_value=0
                temp_key=0
                for j in range(len(df_team_list[k])):
                    temp = abs(d-df_team_list[k]['game_unix_timestamp'][j])
                    if temp<distance:
                        temp_key=j
                        distance=temp
                df_team_list[k]['score'][temp_key]=df2['score'][i]
                df_team_list[k]['num_comments'][temp_key]=df2['num_comments'][i]
                df_team_list[k]['title'][temp_key]=df2['title'][i]
    print(k)
with open('df201213.pkl', 'wb') as f:  #<-change season here
    pickle.dump(df_team_list, f)
'''  
with open('df201718.pkl', 'rb') as f: #<-change season here
    df_team_list = pickle.load(f)

#i=35
#print(df_team_list[9]['title'][i],df_team_list[9]['visitorTeam'][i])
print((df_team_list))
'''  
        

    