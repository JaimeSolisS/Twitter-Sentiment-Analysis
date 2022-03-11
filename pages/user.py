import streamlit as st
from pages.auth import auth
from pages.data import getData_fromUser
from pages.data_processing import createDF
from pages.visuals import sentimentScatter, sentimentPie, getMask,generate_better_wordcloud, typePie, show_tweets

def app():
    api = auth()
   
    st.sidebar.header('Specify Parameters')
    full_username = st.sidebar.text_input("Username (with @)")
    error_slot = st.sidebar.empty() 
    count = st.sidebar.slider('# of tweets', 100,3200,100, key="amount")
    count_slot = st.sidebar.empty()
    if count > 2000:
        count_slot.warning("This amount of tweets may take more than a mintue to process.")
    else: 
        count_slot.empty()
    replies = st.sidebar.selectbox("Include replies", ("false", "true")) #you will receive up-to count tweets — this is because the count parameter retrieves that many Tweets before filtering out retweets and replies.
    rts = st.sidebar.selectbox("Include RTs", ("false", "true")) #When set to false , the timeline will strip any native retweets (though they will still count toward both the maximal length of the timeline and the slice selected by the count parameter).
    translate_slot = st.sidebar.empty()
    more_options = st.sidebar.checkbox('Show more options')
    stop_words_slot = st.sidebar.empty()
    custom_stop_words_slot = st.sidebar.empty()
    tweets_toShow_slot = st.sidebar.empty()
    
    use_custom_stop_words = ""
    translate = "false"
    
    if more_options:
        use_custom_stop_words = custom_stop_words_slot.text_area('Custom stop words', value='', placeholder="e.g. words, world, youd, youre")
        tweets_toShow = tweets_toShow_slot.slider('# of sample tweets', 5,25,5, key="show")
        if (count < 300):
            translate = st.sidebar.selectbox("Translate tweets", ("false", "true"))    
    else:
        stop_words_slot.empty()
        custom_stop_words_slot.empty()
        tweets_toShow = 5
 

    submit = st.sidebar.button("Submit") 

    # Originally it is exclude_replies in Twitter API, so we need to invert it to be consistent with include_rts
    if replies == "false":
        replies = "true"
    else: 
        replies= "false"

    slot1 = st.empty()
    slot2 = st.empty()
    slot3 = st.empty()
    slot4 = st.empty()
    slot5 = st.empty()
    slot6 = st.empty()
    slot7 = st.empty()
    slot8 = st.empty()

    slot1.write('In this page, we will analyze tweets from a specific user.')
    slot2.write('Requesting tweets from protected users or non-existent users will result in an error.')
    slot3.write("This method can only return up to 3,200 of a user's most recent Tweets. Native retweets of other statuses by the user is included in this total, regardless of whether `Include RTs` is set to false when requesting this resource.")
    slot4.write('Using `Include replies` and `Include RTs` set to *false* with will mean you will receive up-to _# of tweets_ tweets — this is because the count parameter retrieves that many Tweets before filtering out retweets and replies.')
    slot5.write('Click the *Show more options* checkbox to display more configurations like *Custom Stop Words* or the *Translate tweets* options!')
    slot6.write('To create the *word cloud* I used the built-in stop words list from the wordcloud library (you can see the whole list on its [repository](https://github.com/amueller/word_cloud/blob/master/wordcloud/stopwords)). But also by writting comma-separated words in the `Custom stop words` text area you can specify more words!')
    slot7.write('''>  “*Stop words are **a set of commonly used words in a language**. 
                        Examples of stop words in English are “a”, “the”, “is”, “are” and etc. 
                    Stop words are commonly used in Text Mining and Natural Language Processing (NLP) 
                    to eliminate words that are so commonly used that they carry very little useful information."— just googled that*. ''')
    slot8.write('Use `Translate Tweets` set to true **ONLY** if you want to analyze users who tweet in another language other than english as it may take a bit to translate the tweets. It is only possible to translate up to 300 tweets for now.')

    if submit: 
        try:
            if full_username[0] != "@":
                error_slot.error("Please, don't forget the @")
            else:
                slot1.empty()
                slot2.empty()
                slot3.empty()
                slot4.empty()
                slot5.empty()
                slot6.empty()
                slot7.empty()
                slot8.empty()
                username = full_username[1:]
               
                # Extract tweets from the twitter user 
                posts = []
                try:
                    getData_fromUser(api,posts, username, replies, rts, count)                 
                        
                    st.header(f"Analyzing the Timeline of: **{full_username}** ...")
                    
                    df = createDF(posts, translate)  
                    #st.dataframe(df)
                    #st.header("Rendering charts")
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
        except:
            st.error("Something went wrong 😞")
        


