import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import pickle
from datetime import datetime, timedelta, timezone

for number in (2019,2018,2017,2016,2015,2014,2013):
    year = number   # season=> (year-1)-(year)
    month_string=['october','november','december','january','february','march','april']
    #month_string1112=['december','january','february','march','april']
    URL=[]
    for month in range(len(month_string)):
        URL.append('https://www.basketball-reference.com/leagues/NBA_'+str(year)+'_games-'+month_string[month]+'.html')
    
    year_list=[]
    for url in URL:
        resp=requests.get(url)
        soup=BeautifulSoup(resp.text, 'html5lib')
        length = len(soup.find_all('tbody')[0].find_all('tr'))
        
        
        month_list = []
        for i in range(length):
            playoff = soup.find_all('tbody')[0].find_all('tr')[i].text
            if (playoff=='Playoffs'):
                break
            date = soup.find_all('tbody')[0].find_all('tr')[i].find_all('th')[0].text        
            start_time = soup.find_all('tbody')[0].find_all('tr')[i].find_all('td')[0].text
            start_time = start_time+'m'
            gameDateEst = date+start_time
            visitorTeam = soup.find_all('tbody')[0].find_all('tr')[i].find_all('td')[1].text
            #visitorScore = soup.find_all('tbody')[0].find_all('tr')[i].find_all('td')[2].text
            homeTeam = soup.find_all('tbody')[0].find_all('tr')[i].find_all('td')[3].text
            #homeScore = soup.find_all('tbody')[0].find_all('tr')[i].find_all('td')[4].text
            attend = soup.find_all('tbody')[0].find_all('tr')[i].find_all('td')[7].text
            attend = int(attend.replace(attend[-4],""))
            
            if homeTeam=='New Jersey Nets':
                homeTeam='Brooklyn Nets'
            if homeTeam=='Charlotte Bobcats':
                homeTeam='Charlotte Hornets'
            if homeTeam=='New Orleans Hornets':
                homeTeam='New Orleans Pelicans'
            if visitorTeam=='New Jersey Nets':
                visitorTeam='Brooklyn Nets'
            if visitorTeam=='Charlotte Bobcats':
                visitorTeam='Charlotte Hornets'
            if visitorTeam=='New Orleans Hornets':
                visitorTeam='New Orleans Pelicans'
            
            temp ={'gameDateEst':gameDateEst,'visitorTeam':visitorTeam,
                   'homeTeam':homeTeam, 'attend':attend}
            month_list.append(temp)
        year_list.append(month_list)
    '''
    with open('nba_crawler.pkl', 'wb') as f:  #<-change season here
        pickle.dump(year_list, f)
    
    with open('nba_crawler.pkl', 'rb') as f: #<-change season here
        year_list = pickle.load(f)
    '''
    
    df=pd.DataFrame()
    for a in range(len(year_list)):
        df2=pd.DataFrame(year_list[a])
        df=df.append(df2)
    
    
    
    with open('teams.json') as json_file:  
        team_data = json.load(json_file)
    iterable=[]
    for b in range(len(team_data)):
        iterable.append((team_data[b]['teamName'],team_data[b]['teamId']))
    team_dic={key: value for (key, value) in iterable}
    def name_to_id(ID):
        return team_dic[ID]
    
    def string_to_datetime(string):
        date_object = datetime.strptime(string, '%a, %b %d, %Y%I:%M%p')
        return date_object
    
    df['homeTeamId']=df['homeTeam']
    df['visitorTeamId']=df['visitorTeam']
    df['homeTeamId']=df['homeTeamId'].apply(name_to_id)
    df['visitorTeamId']=df['visitorTeamId'].apply(name_to_id)
    df['season']=year
    df['gameDateEst']=df['gameDateEst'].apply(string_to_datetime)
    
    df_team_list=[]
    for team, df_team in df.groupby('homeTeam'):
        temp=df_team.reset_index(drop=True)
        df_team_list.append(temp)
    #print(len(df_team_list))
    
    with open('schedule'+str(year-1)+str(year)+'.pkl', 'wb') as f:  #<-change season here
        pickle.dump(df_team_list, f)
    print(str(year-1)+str(year))