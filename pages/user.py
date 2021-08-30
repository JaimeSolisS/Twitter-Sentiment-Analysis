import streamlit as st

def app():
    st.title('User')

    st.write('This is the `user analysis page` of this multi-page app.')

    st.write('In this page, we will be analyze tweets from a specific user')

    st.sidebar.header('Specify Input Parameters')
