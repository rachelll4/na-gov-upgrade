import tweepy
import os
import pandas as pd
from datetime import datetime

c_key = os.environ['TWEEPY_API_KEY']
c_secret = os.environ['TWEEPY_API_SECRET']
token_key = os.environ['TWEEPY_ACCESS_TOKEN']
token_secret = os.environ['TWEEPY_ACCESS_TOKEN_SECRET']

client = tweepy.Client(consumer_key =  c_key,
                        consumer_secret = c_secret,
                        access_token = token_key,
                        access_token_secret = token_secret)

try:
    new_data = pd.read_csv('./data/new_cases.csv')
except pd.errors.EmptyDataError:
    new_data = pd.DataFrame()


#new_data = pd.DataFrame([['2021-00000011', '1/1/2021 1:16', '1/1/2021 1:16', 'Emergency Petition', 'CBE', 'Baltimore Ave / College Ave']])
#print(new_data)

try:
    updated_data = pd.read_csv('./data/updated-activities.csv')
except pd.errors.EmptyDataError:
    updated_data = pd.DataFrame()

#columns = [UMPD CASENUMBER,	OCCURRED DATE TIMELOCATION,	REPORT DATE TIME,	TYPE,	DISPOSITION,	LOCATION]

if len(new_data) > 0:
    total = 0
    for row in new_data.itertuples():
        occur_date = datetime.strptime(row[2], "%m/%d/%Y %H:%M")
        report_date = datetime.strptime(row[3], "%m/%d/%Y %H:%M")
        text = row[4] + " reportedly occurred at " + row[6] + " on " + occur_date.strftime("%b %d, %Y") + ", and is currently "+ row[5]+ ". It was reported on " + report_date.strftime("%b %d, %Y")+ "."
        print(text)
        response = client.create_tweet( text = text )
        print(response)

    text = "Hello world! This is yet another automated tweet!"
    print(text)
else:
    text = "There is no new UMPD activity from yesterday."
    response = client.create_tweet( text = text )
    print(response)


