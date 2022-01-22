from numpy.core import machar
import streamlit as st
from tensorflow.python.ops.gen_array_ops import empty, placeholder
import tweepy
import pandas as pd
import re
from textblob import TextBlob 
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import numpy as np
from PIL import Image
import requests
import streamlit.components.v1 as components
from deep_translator import GoogleTranslator
import time
from stqdm import stqdm

# Set Colors 
blue = "#1DA1F2"
black = "#14171A"
dark_gray = "#657786"
light_gray = "#AAB8C2"

#Modify Colormap
color_map = plt.cm.get_cmap('Blues', 256).reversed()
new_color_map = ListedColormap(color_map(np.linspace(0, .7, 256)))

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

# Create Function to identify Organic Tweets
st.cache
def organic(df):
    if (df['is_reply'] is None) and (df['is_retweeted'] is False) and (df['is_quote'] is False):
        return True
    else: 
        return False
# Create Function to identify Reeweets
st.cache
def rt(df):
    if (df['Tweet'][0:2] == "RT") :
        return True
    else: 
        return False  

# Create Function to clasify tweets based on the rest of columns 
st.cache
def tweetype(df):
    if (df['is_reply'] != None):
        return 'Reply'
    elif (df['is_retweeted'] is True):
        return 'Retweet'
    elif (df['is_quote'] is True):
        return 'Quote'
    else:
        return 'Organic'

# Create a function to clean the tweets
st.cache
def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9_]+', '', text) #Removing @mentions
    text = re.sub('#', '', text) # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text) # Removing RT
    text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
    return text 

# Create a function to get the subjectivity
st.cache
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity
st.cache
def getPolarity(text):
    return  TextBlob(text).sentiment.polarity

# Create a function to compute negative (-1), neutral (0) and positive (+1) analysis
st.cache
def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

# Create a function to translate
st.cache
def translateTweet(text):
    return GoogleTranslator(source='auto', target='en').translate(text)

# Create function to store translated tweets in a DataFrame
st.cache
def translateTweets(tweets): 
    translated_tweets =[]
    
    text = st.empty()
    bar = st.empty()
    
    text.header("Translating tweets...")
    bar.progress(0)
    count = len(tweets)
    
    index = 0
    for tweet in tweets:
        translated_tweets.append(translateTweet((tweet.full_text)))
        index += 1
        bar.progress(((index*100)/count)/100)     
    df = pd.DataFrame(translated_tweets)
    df['Tweets_Translated'] = pd.Series(df.fillna('').values.tolist()).str.join('')
    df.drop(df.columns.difference(['Tweets_Translated']), 1, inplace=True)

     # Clear screen
    text.empty()
    bar.empty()
    return df

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
    
st.cache
def createDF(posts, translate): 
    bar = st.empty()
    bar.progress(0)
    # Create a dataframe with a column called Tweets
    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweet'])
    for percent_complete in range(7):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)

    if translate == "true":
        df['Tweets_Translated'] = translateTweets(posts)
        for percent_complete in range(7,14):
            bar.progress(percent_complete + 1)
            time.sleep(0.1)
    # Replace some NaN values, don't know why
    #df.Tweets_Translated.fillna(df.Tweet, inplace=True)
    df['id'] = pd.DataFrame([tweet.id for tweet in posts])
    for percent_complete in range(14,21):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['screen_name'] = pd.DataFrame([tweet.user.screen_name for tweet in posts])
    for percent_complete in range(21,28):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['is_reply'] = pd.DataFrame([tweet.in_reply_to_screen_name for tweet in posts])
    for percent_complete in range(28,35):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['is_retweeted'] = df.apply(rt, axis=1)
    for percent_complete in range(35,42):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['is_quote'] = pd.DataFrame([tweet.is_quote_status for tweet in posts])
    for percent_complete in range(42,49):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['is_organic'] = df.apply(organic, axis=1)
    for percent_complete in range(49,56):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['Type'] =df.apply(tweetype, axis=1)
    for percent_complete in range(56,63):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)

    if translate == "true":
        # Clean the tweets
        df['clean_Tweet'] = df['Tweets_Translated'].apply(cleanTxt)
        for percent_complete in range(63,70):
            bar.progress(percent_complete + 1)
            time.sleep(0.1)
        df['clean_Tweet_original'] = df['Tweet'].apply(cleanTxt)
        for percent_complete in range(70,77):
            bar.progress(percent_complete + 1)
            time.sleep(0.1)
    else: 
        # Clean the tweets
        df['clean_Tweet'] = df['Tweet'].apply(cleanTxt)
        for percent_complete in range(63,70):
            bar.progress(percent_complete + 1)
            time.sleep(0.1)
        df['clean_Tweet_original'] = df['Tweet'].apply(cleanTxt)
        for percent_complete in range(70,77):
            bar.progress(percent_complete + 1)
            time.sleep(0.1)


    #df['Tweets_Translated'] = df['Tweets_Translated'].apply(cleanTxt)
    # Create two new columns 'Subjectivity' & 'Polarity'
    df['Subjectivity'] = df['clean_Tweet'].apply(getSubjectivity)
    for percent_complete in range(77,84):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['Polarity'] = df['clean_Tweet'].apply(getPolarity)
    for percent_complete in range(84,91):
        bar.progress(percent_complete + 1)
        time.sleep(0.1)
    df['Analysis'] = df['Polarity'].apply(getAnalysis)
    for percent_complete in range(91,100):
        bar.progress(percent_complete + 1)
        time.sleep(0.1) 
    time.sleep(1)
    bar.empty()
    return df
st.cache
def sentimentPie(df):
    df1 = df.groupby('Analysis').count()[['Tweet']].reset_index()
    fig = px.pie(df1, 
                values='Tweet', 
                names='Analysis', 
                color='Analysis', 
                color_discrete_map={'Positive': blue,
                                    'Negative': black,
                                    'Neutral': dark_gray}, 
                hole=.4, 
                )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update(layout_showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
st.cache
def typePie(df):
    df1 = df.groupby('Type').count()[['Tweet']].reset_index()

    fig = px.pie(df1, 
                values='Tweet', 
                names='Type', 
                color='Type', 
                color_discrete_map={'Organic': blue,
                                    'Retweet': black,
                                    'Quote': dark_gray,
                                    'Reply': light_gray }, 
                hole=.4, 
                )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update(layout_showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
st.cache
def sentimentScatter(df): 
    
    #Since plotly reads in html including tags, \n and the break tag <br> can be inserted into the text for the df variable you want to have wrap when displayed:
    df.Tweet = df.Tweet.str.wrap(60)
    df.Tweet = df.Tweet.apply(lambda x: x.replace('\n', '<br>'))
    fig = px.scatter(df, x="Polarity", y="Subjectivity", 
                 color="Type",
                 hover_data=['Tweet'],
                color_discrete_map={
                "Organic": blue,
                "Retweet": black,
                "Quote": dark_gray,
                "Reply": light_gray,
                },)

    st.markdown("""
    **Subjectivity**: how subjective or opinionated a tweet is (a score of 0 is fact, and a score of +1 is very much an opinion).  
    **Polarity**: how positive or negative a tweet is (a score of -1 is the highest negative score, and a score of +1 is the highest positive score).
    """)
    fig.update_layout(template='plotly_white')
    #fig.update(layout_title_text='Sentiment Analysis')
    st.plotly_chart(fig, use_container_width=True)

    # get percentage
    tweets = df[df.Analysis == 'Positive']
    tweets = tweets['Tweet']
    tweets = round( (tweets.shape[0] / df.shape[0]) * 100 , 1)
    #st.write(tweets)
 
    
    #st.dataframe(df)
st.cache

def generateWordCloud(df):
    # word cloud visualization
    allWords = ' '.join([twts for twts in df['clean_Tweet_original']])
    wordCloud = WordCloud(width=500, height=300, random_state=21, background_color="white", max_words=100, colormap=new_color_map).generate(allWords)
    fig, ax = plt.subplots()
    ax.imshow(wordCloud, interpolation="bilinear")
    ax.axis('off')
    #ax.set_title('Most frequent words found')
    st.pyplot(fig, use_container_width=True)

st.cache
def getMask():
    return np.array(Image.open('img/twitter_mask.png'))

def stopWords():
    with open('stopwords/english.txt', 'r') as f:
         #Define a list of stop words 
        stopWords = [line.strip() for line in f]
        return stopWords
 
st.cache
def generate_better_wordcloud(df, title, use_custom_stop_words, mask=None):

    allWords = ' '.join([twts for twts in df['clean_Tweet_original']])
    custom_stop_words_list = use_custom_stop_words.replace(" ", "").split(",")
    stop_words = custom_stop_words_list + list(STOPWORDS)
    
    cloud = WordCloud(scale=3,
            max_words=500,
            colormap=new_color_map,
            mask=mask,
            background_color='white',
            stopwords=stop_words,
            collocations=True).generate_from_text(allWords)

    fig, ax = plt.subplots()                   
    ax.imshow(cloud, interpolation="bilinear")
    ax.axis('off')
    ax.set_title(title)
    st.pyplot(fig, use_container_width=True)
    
class Tweet(object):
    def __init__(self, s, embed_str=False):
        if not embed_str:
            # Use Twitter's oEmbed API
            # https://dev.twitter.com/web/embedded-tweets
            api = "https://publish.twitter.com/oembed?url={}".format(s)
            response = requests.get(api)
            self.text = response.json()["html"]
        else:
            self.text = s

    def _repr_html_(self):
        return self.text

    def component(self):
        return components.html(self.text, height=600)
st.cache
def show_tweets(df, analysis, sort, tweets_toShow):
    newDF = df[df.Analysis == analysis]
    newDF = newDF.sort_values(by=['Polarity'], ascending=sort) #Sort the tweets
    # Implment this in order to avoid errors
    finished = False
    count = 0
    index = 0
    while not finished:
        try:
            t = Tweet(f"https://twitter.com/{newDF['screen_name'][index]}/status/{newDF['id'][index]}").component()
            index +=1
            count += 1
        except:
            index +=1
        finished = evaluate_end_condition(count, tweets_toShow)
st.cache
def evaluate_end_condition(count, tweets_toShow):
    if count == tweets_toShow:
        return True
    else:
         return False

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
                    getData(api,posts, username, replies, rts, count)
                        
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
        


