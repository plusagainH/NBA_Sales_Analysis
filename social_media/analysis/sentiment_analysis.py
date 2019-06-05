import pandas as pd
import pickle
from datetime import datetime, timedelta, timezone
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()
def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    #print("{:-<40} {}".format(sentence, str(score)))
    return (score['compound'])

with open('team.pkl', 'rb') as f:
    team = pickle.load(f)  #list

df0506=pd.DataFrame() #<-change season here
for i in range(len(team)):
    with open(team[i][0]+'_comment_05-06.pkl', 'rb') as f: #<-change season here
        df = pickle.load(f)
    score_list=[]
    team_name=[]
    season=[]
    for j in range(len(df['comment_text'])):
        score_list.append(sentiment_analyzer_scores(df['comment_text'][j]))
        team_name.append(team[i][0])
        season.append(506)  #<-change season here
    df["sentiment_score"] = score_list
    df["team"]=team_name
    df["season"]=season
    df0506 = df0506.append(df, ignore_index=True)  #<-change season here
with open('df0506.pkl', 'wb') as f:  #<-change season here
    pickle.dump(df0506, f)  #<-change season here