import pandas as pd
import pickle
import numpy as np
from datetime import datetime, timedelta, timezone
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()
def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    #print("{:-<40} {}".format(sentence, str(score)))
    return (score['compound'])

with open('team.pkl', 'rb') as f:
    team = pickle.load(f)  #list
    

team_score=[]
for i in range(len(team)):
    with open(team[i][0] +'_comment_10-11.pkl', 'rb') as f:
        df = pickle.load(f)
    score_list=[]
    for j in range(len(df['comment_text'])):
        score_list.append(sentiment_analyzer_scores(df['comment_text'][j]))
    weighting=0
    b =0
    for k in range(len(score_list)):
        weighting = weighting + score_list[k]*(df["comment_score"][k]+1)
        b=b+(df["comment_score"][k]+1)
    team_score.append(weighting/b)

home_attendance=[]
for m in range(30):
    home_attendance.append(team[m][3])

print(np.corrcoef(team_score,home_attendance))


    
