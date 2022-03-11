import streamlit as st
from pages.auth import auth
from pages.data import getData_fromQuery
from pages.data_processing import createDF
from pages.visuals import sentimentScatter, sentimentPie, getMask,generate_better_wordcloud, typePie, show_tweets

def app():

    st.sidebar.header('Specify Input Parameters')
    query = st.sidebar.text_input("Term to search")
    error_slot = st.sidebar.empty()
    count = st.sidebar.slider('# of tweets', 100,3200,100, key="amount")
    count_slot = st.sidebar.empty()
    if count > 2000:
        count_slot.warning("This amount of tweets may take more than a mintue to process.")
    else: 
        count_slot.empty()
    if (count < 300):
            lang = st.sidebar.selectbox("Language", ("en", "es", "fr"))
    else:
        lang = "en"
    result_type = st.sidebar.selectbox("Result Type", ("mixed", "recent", "popular"))
    
    
    more_options = st.sidebar.checkbox('Show more options')
    stop_words_slot = st.sidebar.empty()
    custom_stop_words_slot = st.sidebar.empty()
    tweets_toShow_slot = st.sidebar.empty()
    
    use_custom_stop_words = ""
    
    if more_options:
        use_custom_stop_words = custom_stop_words_slot.text_area('Custom stop words', value='', placeholder="e.g. words, world, youd, youre")
        tweets_toShow = tweets_toShow_slot.slider('# of sample tweets', 5,25,5, key="show")
        
    else:
        stop_words_slot.empty()
        custom_stop_words_slot.empty()
        tweets_toShow = 5

    if lang == "en":
        translate = "false"
    else:
        translate = "true"
 

    submit = st.sidebar.button("Submit") 


    slot1 = st.empty()
    slot2 = st.empty()
    slot3 = st.empty()
    slot4 = st.empty()
    slot5 = st.empty()

    slot1.write('In this page, we will analyze tweets that contain a specic word, phrase or hashtag')
    slot2.write("Please note that Twitter's search service and, by extension, the Search API used in this project is not meant to be an exhaustive source of Tweets. Not all Tweets will be indexed or made available via the search interface.")

    if submit:
        try:
            api = auth()
            slot1.empty()
            slot2.empty()
            slot3.empty()
            slot4.empty()
            slot5.empty()

            posts = []
            getData_fromQuery(api,posts, query, count, lang, result_type)  
            posts = api.search(q=query, count = count, lang=lang, tweet_mode="extended", result_type=result_type)
            st.header(f"Analyzing tweets with: **{query}** ...")
            df = createDF(posts, translate)  

            st.subheader("Polarity and Subjectivity")
            sentimentScatter(df)

            col1, col2 = st.columns([1,1])
            with col1:
                st.subheader("Tweets Classification by Sentiment")
                sentimentPie(df)
            with col2:
                st.subheader("Tweets Classification by Type")
                typePie(df)
            st.subheader("Most frequent Words")
            generate_better_wordcloud(df, "", use_custom_stop_words, mask=getMask())

            col1, col2 = st.columns([1,1])
            with col1:
                st.subheader("Some Positive tweets")
                show_tweets(df, "Positive", False, tweets_toShow)
            with col2:
                st.subheader("Some Negative tweets")
                show_tweets(df, "Negative", True, tweets_toShow)
        
        except:
            st.error("Something went wrong 😞")
