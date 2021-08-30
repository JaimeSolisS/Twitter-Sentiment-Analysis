import streamlit as st

def app():
    st.title('Search')

    st.write('This is the `Search analysis page` of this multi-page app.')

    st.write('In this page, we will be analyze tweets that contain a specif word, phrase or hastag')

    st.sidebar.header('Specify Input Parameters')
