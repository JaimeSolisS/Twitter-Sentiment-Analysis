import streamlit as st
import tweepy

st.cache
def getData(api, posts, username, replies, rts, count):
    text = st.empty()
    bar = st.empty()
    text.header("Getting Data...")
    bar.progress(0)
    index = 0

    # For 200 tweets or less
    #posts = api.user_timeline(screen_name=username, count = count, exclude_replies=replies, include_rts=rts, tweet_mode="extended")

    # For more than 200 tweets
    for items in tweepy.Cursor(api.user_timeline, screen_name=username, exclude_replies=replies, include_rts=rts, tweet_mode="extended").items(count):
        posts.append(items)
        index += 1
        bar.progress(index/count)

    # Clear screen
    text.empty()
    bar.empty()

    return  