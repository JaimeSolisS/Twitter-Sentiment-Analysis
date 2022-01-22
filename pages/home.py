import streamlit as st

def app():
    st.markdown("""
    Hi! Welcome to my Twitter Sentiment Analysis App. This app
    parses the tweets from **a specific user** or tweets that contain **a specific word, phrase or hashtag** including:   
    
    - Polarity and Subjectivity 
    - Classification by Sentiment (Positive, Neutral or Negative)
    - Classification by Type (Organic, Quotes, Replies and RTs) 
    - Most Frequent Words used

    After these graphs, you will find some samples of positive and negative tweets.  

    All this data comes from the Twitter API and none is stored by this app 😉.
   
    """)

 
    st.write('''>  “**Sentiment analysis**: *the process of computationally identifying 
    and categorizing opinions expressed in a piece of text, especially in order 
    to determine whether the writer’s attitude towards a particular topic, product, 
    etc. is positive, negative, or neutral.”— Oxford English Dictionary* ''')
  
    st.write("👈 To begin, plese select either **User** or **Search** from the sidebar.")
