import streamlit as st
import tweepy
import pandas as pd
import time
from deep_translator import GoogleTranslator
import re
from pages.data_analysis import *

# Create a function to translate
st.cache
def translateTweet(text):
    return GoogleTranslator(source='auto', target='en').translate(text)

# Create function to store translated tweets in a DataFrame
st.cache
def translateTweets(tweets): 
    translated_tweets =[]
    
    text = st.empty()
    bar = st.empty()
    
    text.header("Translating tweets...")
    bar.progress(0)
    count = len(tweets)
    
    index = 0
    for tweet in tweets:
        translated_tweets.append(translateTweet((tweet.full_text)))
        index += 1
        bar.progress(((index*100)/count)/100)     
    df = pd.DataFrame(translated_tweets)
    df['Tweets_Translated'] = pd.Series(df.fillna('').values.tolist()).str.join('')
    df.drop(df.columns.difference(['Tweets_Translated']), 1, inplace=True)

     # Clear screen
    text.empty()
    bar.empty()
    return df

# Create Function to identify Organic Tweets
st.cache
def organic(df):
    if (df['is_reply'] is None) and (df['is_retweeted'] is False) and (df['is_quote'] is False):
        return True
    else: 
        return False
# Create Function to identify Reeweets
st.cache
def rt(df):
    if (df['Tweet'][0:2] == "RT") :
        return True
    else: 
        return False  

# Create Function to clasify tweets based on the rest of columns 
st.cache
def tweetype(df):
    if (df['is_reply'] != None):
        return 'Reply'
    elif (df['is_retweeted'] is True):
        return 'Retweet'
    elif (df['is_quote'] is True):
        return 'Quote'
    else:
        return 'Organic'

# Create a function to clean the tweets
st.cache
def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9_]+', '', text) #Removing @mentions
    text = re.sub('#', '', text) # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text) # Removing RT
    text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
    return text 

st.cache
def createDF(posts, translate): 
    bar = st.empty()
    bar.progress(0)
    # Create a dataframe with a column called Tweets
    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweet'])
    for percent_complete in range(7):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)

    if translate == "true":
        df['Tweets_Translated'] = translateTweets(posts)
        for percent_complete in range(7,14):
            bar.progress(percent_complete + 1)
            time.sleep(0.1)
    # Replace some NaN values, don't know why
    #df.Tweets_Translated.fillna(df.Tweet, inplace=True)
    df['id'] = pd.DataFrame([tweet.id for tweet in posts])
    for percent_complete in range(14,21):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['screen_name'] = pd.DataFrame([tweet.user.screen_name for tweet in posts])
    for percent_complete in range(21,28):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['is_reply'] = pd.DataFrame([tweet.in_reply_to_screen_name for tweet in posts])
    for percent_complete in range(28,35):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['is_retweeted'] = df.apply(rt, axis=1)
    for percent_complete in range(35,42):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['is_quote'] = pd.DataFrame([tweet.is_quote_status for tweet in posts])
    for percent_complete in range(42,49):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['is_organic'] = df.apply(organic, axis=1)
    for percent_complete in range(49,56):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['Type'] =df.apply(tweetype, axis=1)
    for percent_complete in range(56,63):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)

    if translate == "true":
        # Clean the tweets
        df['clean_Tweet'] = df['Tweets_Translated'].apply(cleanTxt)
        for percent_complete in range(63,70):
            bar.progress(percent_complete + 1)
            time.sleep(0.1)
        df['clean_Tweet_original'] = df['Tweet'].apply(cleanTxt)
        for percent_complete in range(70,77):
            bar.progress(percent_complete + 1)
            time.sleep(0.1)
    else: 
        # Clean the tweets
        df['clean_Tweet'] = df['Tweet'].apply(cleanTxt)
        for percent_complete in range(63,70):
            bar.progress(percent_complete + 1)
            time.sleep(0.1)
        df['clean_Tweet_original'] = df['Tweet'].apply(cleanTxt)
        for percent_complete in range(70,77):
            bar.progress(percent_complete + 1)
            time.sleep(0.1)


    #df['Tweets_Translated'] = df['Tweets_Translated'].apply(cleanTxt)
    # Create two new columns 'Subjectivity' & 'Polarity'
    df['Subjectivity'] = df['clean_Tweet'].apply(getSubjectivity)
    for percent_complete in range(77,84):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['Polarity'] = df['clean_Tweet'].apply(getPolarity)
    for percent_complete in range(84,91):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['Analysis'] = df['Polarity'].apply(getAnalysis)
    for percent_complete in range(91,100):
        bar.progress(percent_complete + 1)
        time.sleep(0.1) 
    time.sleep(1)
    bar.empty()
    return df

