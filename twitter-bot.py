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
    new_data = pd.read_csv('./data/new_cases.csv', sep = ';')
except pd.errors.EmptyDataError:
    new_data = pd.DataFrame()
    
arrest_data = pd.read_csv('./data/all-police-arrests.csv')

try:
    updated_data = pd.read_csv('./data/updated-activities.csv', sep =";")
except pd.errors.EmptyDataError:
    updated_data = pd.DataFrame()

#columns = [UMPD CASENUMBER,	OCCURRED DATE TIMELOCATION,	REPORT DATE TIME,	TYPE,	DISPOSITION,	LOCATION]

tweet_id = None
print(len(arrest_data))

if len(new_data) > 0:
    total = 0
    for row in new_data.itertuples():
    
        disposition = row[5]
        if disposition == "CBE":
            disposition = "closed"
            
        spot = ""
        if str(row[6]) != "nan" and ',' in row[6]:
            for item in row[6].split(','):
                if len(item) > len(spot):
                    spot = item.strip()
        else:
            spot = row[6]
            if str(spot) == "nan":
                spot = "in an undisclosed location"
        
        occur_date = ""
        try:
            occur_date = datetime.strptime(row[2], "%m/%d/%Y %H:%M")
        except: 
            try:
                occur_date = datetime.strptime(row[2], "%m/%d/%y %H:%M")
            except:
                try:
                    occur_date = datetime.strptime(row[2], "%m/%d/%Y")
                except:
                    try: 
                        occur_date = datetime.strptime(row[2], "%m/%d/%y")
                    except:
                        occur_date = "unknown time"
            
        report_date = ""
        try:
            report_date = datetime.strptime(row[3], "%m/%d/%Y %H:%M")
        except: 
            try:
                report_date = datetime.strptime(row[3], "%m/%d/%y %H:%M")
            except:
                try:
                    report_date = datetime.strptime(row[3], "%m/%d/%Y")
                except:
                    try: 
                        report_date = datetime.strptime(row[3], "%m/%d/%y")
                    except:
                        report_date = "unknown time"
        
        text = "On " + occur_date.strftime("%b %d, %Y") + ", "+ row[4] + " was reported at " + spot + ". The case, now labeled "+ disposition+ ", was reported on " + report_date.strftime("%b %d, %Y")+ "."
        
        if disposition == "Arrest":
            arrest = []
            for arrest_item in arrest_data.itertuples(): 
                if str(arrest_item[3]) == str(row[1]):
                    arrest = arrest_item
                    break
                    
            if len(arrest) != 0:
                charges = arrest[7].split(';')
                text += "\nA "
                if str(arrest[4]) != "nan":
                    text += str(arrest[4]) + "-year-old "
                if str(arrest[5]) != "nan":
                    text += arrest[5]
                if str(arrest[6]) != "nan":
                    text += " " + arrest[6]
                else:
                    text += "person"
                text += " was arrested on these charges: " 
                for charge in charges:
                    text += charge + ".\n"
        
        print(text)
        # if tweet_id == None:
            # response = client.create_tweet( text = text)
            # print(response)
        # else:
            # response = client.create_tweet( text = text, quote_tweet_id = tweet_id)
        # tweet_id = response.id

# else:
    # text = "There is no new UMPD activity from yesterday."
    # response = client.create_tweet( text = text )
    # print(response)


