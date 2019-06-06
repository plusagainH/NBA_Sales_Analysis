import json
import requests
import praw
import pandas as pd
import time
import pickle
from operator import itemgetter
from datetime import datetime, timedelta, timezone

start = time.time()

with open('team.pkl', 'rb') as f:
    team = pickle.load(f)  #list

for i in range(len(team)):
    reddit_name = team[i][1]
    team_name = team[i][0]
    
    game_start_date = datetime(2005,10,21,0,0,0)  #<-change season here
    game_end_date = datetime(2006,4,19,23,59,59) #<-change season here
    start_date = game_start_date
    end_date = game_start_date
    timestamp=[]
    timestamp.append(int(game_start_date.timestamp()))
    while end_date<game_end_date:
        end_date = start_date + timedelta(days=20)
        t = end_date.timestamp()
        timestamp.append(int(t))
        start_date = end_date
    timestamp[-1] = int(game_end_date.timestamp())
    
    uri=[]
    i=0
    for i in range(len(timestamp)-1):
        uri.append('https://api.pushshift.io/reddit/search/submission?subreddit='+reddit_name+'&after='+str(timestamp[i])+'&before='+str(timestamp[i+1])+'&size=1000')
    
    post = []  #dictionary in list
    j=0
    for j in range(len(uri)):
        response = requests.get(uri[j])
        print(uri[j])
        content = json.loads(response.content)
        for k in range(len(content['data'])):
            post.append(content['data'][k])
            
    with open(team_name+'_post0506.pkl', 'wb') as f:  #<-change season here
        pickle.dump(post, f)
    
    with open(team_name+'_post0506.pkl', 'rb') as f: #<-change season here
        post = pickle.load(f)
        
    post = sorted(post, key=itemgetter('num_comments'))[-4:-1]
    
    reddit = praw.Reddit(client_id='YOUR_ID',
                         client_secret='YOUT_SECRET',
                         user_agent='crawler',
                         username='YOUR_USERNAME',
                         password='YOUR_PASSWORD')
    
    submissions=[]
    m=0
    for m in range(len(post)):
        post_id = post[m]['id']
        submissions.append(reddit.submission(id=post_id))
    
    title = []
    article = []
    comm_author = []
    comm_list = []
    comm_created_utc = []
    comm_link = []
    comm_score = []
    print("get ready")
    for submission in submissions:
        submission.comments.replace_more(limit=0)
        comment_queue = submission.comments[:]  
        while comment_queue:
            comment = comment_queue.pop(0)
            title.append(submission.title)
            article.append(submission.selftext)
            comm_author.append(comment.author)
            comm_list.append(comment.body)
            comm_created_utc.append(comment.created_utc)
            comm_link.append(comment.permalink)
            comm_score.append(comment.score)
            a = []
            a.extend(comment.replies)
            while a:
                reply1 = a.pop(0)
                title.append(submission.title)
                article.append(submission.selftext)
                comm_author.append(reply1.author)
                comm_list.append(reply1.body)
                comm_created_utc.append(reply1.created_utc)
                comm_link.append(reply1.permalink)
                comm_score.append(reply1.score)
        print("one loop finished")
    df = pd.DataFrame({'title':title,
                       'article':article,
                       'comment_author':comm_author,
                       'comment_text':comm_list,
                       'comment_utc':comm_created_utc,
                       'comment_link':comm_link,
                       'comment_score':comm_score})
    with open(team_name+'_comment_05-06.pkl', 'wb') as f:  #<-change season here
        pickle.dump(df, f)
    print("one team finish")
end = time.time()
print(end - start)
