import streamlit as st
from tensorflow.python.ops.gen_array_ops import empty
import tweepy
import os
from dotenv import load_dotenv
import pandas as pd

def auth(): 
    load_dotenv()
    apiKey = os.getenv('CONSUMER_KEY')
    apiSecretKey= os.getenv('CONSUMER_SECRET')
    accessToken= os.getenv('ACCESS_TOKEN')
    AccessTokenSecret = os.getenv('ACCESS_TOKEN_SECRET')

    # create authentication object
    authenticate = tweepy.OAuthHandler(apiKey, apiSecretKey)
    authenticate.set_access_token(accessToken, AccessTokenSecret )
    return tweepy.API(authenticate)

def app():
    api = auth()
    st.title('By User')


    st.sidebar.header('Specify Parameters')
    full_username = st.sidebar.text_input("Username (with @)")
    count = st.sidebar.slider('# of tweets', 10,3200,100)
    replies = st.sidebar.selectbox("Include replies", ("false", "true")) #you will receive up-to count tweets — this is because the count parameter retrieves that many Tweets before filtering out retweets and replies.
    rts = st.sidebar.selectbox("Include RTs", ("false", "true"))
    submit = st.sidebar.button("Submit") #When set to false , the timeline will strip any native retweets (though they will still count toward both the maximal length of the timeline and the slice selected by the count parameter).

    # Originally it is exclude_replies in Twitter API, so we need to invert it to be consistent with include_rts
    if replies == "false":
        replies = "true"
    else: 
        replies= "false"

    if submit: 
        try:
            if full_username[0] != "@":
                st.error("Please, don't forget the @")
            else:
                username = full_username[1:]
                st.header(f"Analyzing the Timeline of: **{full_username}**")
                # Extract tweets from the twitter user 
                posts = []
                # For more than 200 tweets
                for items in tweepy.Cursor(api.user_timeline, screen_name=username, exclude_replies=replies, include_rts=rts, tweet_mode="extended").items(count):
                    posts.append(items)
                # For 200 tweets or less
                #posts = api.user_timeline(screen_name=username, count = count, exclude_replies=replies, include_rts=rts, tweet_mode="extended")
                # Create a dataframe with a column called Tweets
                df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
               
                st.dataframe(df)

        except:
            st.error("Please, specify a username")
    else:
        st.write('In this page, we will be analyze tweets from a specific user.')
        st.write('User timelines belonging to protected users may only be requested when the authenticated user either "owns" the timeline or is an approved follower of the owner.')
        st.write("This method can only return up to 3,200 of a user's most recent Tweets. Native retweets of other statuses by the user is included in this total, regardless of whether `Include RTs` is set to false when requesting this resource.")
        st.write('Using `Include replies` and `Include RTs` set to *false* with will mean you will receive up-to _# of tweets_ tweets — this is because the count parameter retrieves that many Tweets before filtering out retweets and replies.')


