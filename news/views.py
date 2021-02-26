from django.shortcuts import render
import requests
import os
from django.conf import settings
import sys
import pickle
import re
from collections import Counter
import tweepy
import json
import nltk
import string
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
#corups is dataset
from nltk.corpus import stopwords
import numpy as np
import random
import string 
import wordninja #split tag
from textblob import TextBlob
from langdetect import detect
from translate import Translator
import re
from profanityfilter import ProfanityFilter
pf = ProfanityFilter()
translation=''
dst=''

# Create your views here.
def extract(request):
    dict={}
    if request.method=='POST':
        place=request.POST['place']
        if(place=="World"):
            WOE_ID=1
        elif(place=="India"):
            WOE_ID=23424848
        elif(place=="Barcelona"):
            WOE_ID=753692
        elif(place=="Bangalore"):
            WOE_ID=2295420
        elif(place=="Lucknow"):
            WOE_ID=2295377
        elif(place=="Chennai"):
            WOE_ID=2295424
        elif(place=="Lahore"):
            WOE_ID=2211177
        elif(place=="Paris"):
            WOE_ID=615702
        elif(place=="London"):
            WOE_ID=44418
        elif(place=="Dubai"):
            WOE_ID=23424738
        else:
            messages.info(request,'Enter a valid place')
            print('enter valid place')
        api = TwitterClient()
        trends=api.api.trends_place(WOE_ID)
        trends = json.loads(json.dumps(trends, indent=1))
        newscount=0
        trendCount=0
        for trend in trends[0]["trends"]:
            trendCount+=1
            if(trendCount>4):
                break
    		# public_tweets = api.api.search(trend["name"].strip('#'),count=2)
            dict[trend["name"].strip('#')]=[]
            for t in api.get_tweets(trend["name"].strip('#'),5):
                dict[trend["name"].strip('#')].append(t)
        return render(request,'extract.html',{'dict':dict})
    else:
        return render(request,'index.html')

# return html page with context dictionary of tweets

class TwitterClient(object): 
    def __init__(self):
    	consumer_key = 'kjfMjfMGWI4X1ZpLjedXLpvSe'
    	consumer_secret = 'usXTaDx5Uu2r0Gqf0gAb7UzUeGBqDwlASOpeke0kkAJGHo7fHA'
    	access_token = '994471668-AScInzntHQ3m4R1uUiLAf3y9cSZsKCOUOpo9ACPe'
    	access_token_secret = 'vA3WDxZBvH7uHd0xu6SrwYXSkXnbhVWhkyWrOY69fkwLK'
    	try:
    		self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    		self.auth.set_access_token(access_token, access_token_secret)
    		self.api = tweepy.API(self.auth,wait_on_rate_limit=True)
    		print("Successfully Authenticated")
    	except:
    		print("Error: Authentication Failed")

    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())



        

    def get_tweet_emotion(self, tweet):
        text=self.clean_tweet(tweet)
        import re 
        from collections import Counter

        def ngram(token, n): 
            output = []
            for i in range(n-1, len(token)): 
                ngram = ' '.join(token[i-n+1:i+1])
                output.append(ngram) 
            return output


        def create_feature(text, nrange=(1, 1)):
            text_features = [] 
            text = text.lower()
            text_alphanum = re.sub('[^a-z0-9#]', ' ', text)
            for n in range(nrange[0], nrange[1]+1): 
                text_features += ngram(text_alphanum.split(), n)
            
        
            text_punc = re.sub('[a-z0-9]', ' ', text)
            text_features += ngram(text_punc.split(), 1)
            return Counter(text_features)



        dict = {"joy":"😂", "fear":"😱", "anger":"😠", "sadness":"😢", "disgust":"😒", "shame":"😳", "guilt":"😔"}
        import pickle
        loaded_model = pickle.load(open("model.sav", 'rb'))
        vectorizer = pickle.load(open("vec.sav", 'rb'))
        features = create_feature(text, nrange=(1, 4))
        features = vectorizer.transform(features)
        prediction = loaded_model.predict(features)[0]
        return dict[prediction]






    def get_tweet_sentiment(self, tweet):
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 5):  
        tweets = []
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count)
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet
                translation=''
                dst=''
                lang=detect(tweet.text)
                if(lang=='en'):
                    analysis = TextBlob(tweet.text)
                    translation=tweet.text
                    dst='\n <ALREADY IN ENGLISH>'
                else:

                    if lang=='hi':   #try this out #it does not translate if hindi words are lesser than english
                        translator= Translator(from_lang="hindi",to_lang="english")
                        translation = translator.translate(tweet.text)
                        dst='\n <THIS IS TRANSLATED FROM HINDI> \n'
                    if lang=='fr':
                    	translator=Translator(from_lang="french",to_lang="english")
                    	translation = translator.translate(tweet.text)
                    	dst='\n <THIS IS TRANSLATED FROM FRENCH> \n'
                        
                    if lang=='ta':  
                        translator= Translator(from_lang="tamil",to_lang="english")
                        translation = translator.translate(tweet.text)
                        dst='\n <THIS IS TRANSLATED FROM TAMIL> \n'
                    if lang=='es':
                        translator= Translator(from_lang="spanish",to_lang="english")
                        translation = translator.translate(tweet.text)
                        dst='\n <THIS IS TRANSLATED FROM SPANISH> \n'
                analysis = TextBlob(str(translation))
                parsed_tweet['text'] = analysis 
                # saving sentiment of tweet
                parsed_tweet['emotion'] =  self.get_tweet_emotion(tweet.text)
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
                parsed_tweet['lang']=dst
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
