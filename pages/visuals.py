import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import requests
import streamlit.components.v1 as components

# Set Colors 
blue = "#1DA1F2"
black = "#14171A"
dark_gray = "#657786"
light_gray = "#AAB8C2"

#Modify Colormap
color_map = plt.cm.get_cmap('Blues', 256).reversed()
new_color_map = ListedColormap(color_map(np.linspace(0, .7, 256)))

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