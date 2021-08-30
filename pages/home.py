import streamlit as st

def app():
    st.markdown("""
    Hey there! Welcome to Jaime's Twitter Sentiment Analysis App. This app
    parses (never keeps or stores!) the tweets fetched from the Twitter API
    and analyzes data about a specific user or tweets that contain a specific word, phrase or hashtag. 
    """)

    col_1, col_2, col_3 = st.columns([1,4,1])
    with col_1:
        st.write("")
    with col_2:
        st.write('''*“**Sentiment analysis**: *the process of computationally identifying 
    and categorizing opinions expressed in a piece of text, especially in order 
    to determine whether the writer’s attitude towards a particular topic, product, 
    etc. is positive, negative, or neutral.”— Oxford English Dictionary*''')
    with col_3:
        st.write("")  
    st.write("**👈 To begin, plese select a different page from the sidebar.**")