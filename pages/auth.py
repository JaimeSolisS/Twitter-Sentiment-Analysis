import streamlit as st
import tweepy

st.cache
def auth(): 
    apiKey = st.secrets['CONSUMER_KEY']
    apiSecretKey= st.secrets['CONSUMER_SECRET']
    accessToken= st.secrets['ACCESS_TOKEN']
    AccessTokenSecret = st.secrets['ACCESS_TOKEN_SECRET']

    # create authentication object
    authenticate = tweepy.OAuthHandler(apiKey, apiSecretKey)
    authenticate.set_access_token(accessToken, AccessTokenSecret )
    return tweepy.API(authenticate)