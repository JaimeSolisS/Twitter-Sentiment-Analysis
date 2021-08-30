import streamlit as st
from multiapp import MultiApp
from pages import home, user, search # import your app modules here
from PIL import Image 

app = MultiApp()

st.set_page_config(layout="wide")

# Simple grid for gif
col_1, col_2, col_3 = st.columns([2,1,2])
with col_1:
    st.write("")
with col_2:
    st.image('img/twitter-circled-rotation.gif')
with col_3:
    st.write("")

# Simple grid for title
col1, col2 = st.columns([2,1])
with col1: 
    st.title("Analyzing Twitter Data")
with col2: 
    st.write("")
    st.subheader("A Web App by [Jaime Solis](jaimesolis.dev)")

# Add all your application here
app.add_app("Home", home.app)
app.add_app("User", user.app)
app.add_app("Search", search.app)
# The main app
app.run()