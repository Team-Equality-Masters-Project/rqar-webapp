import streamlit as st
import numpy as np
import pandas as pd
from data.sample_data import sample_data
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


def app():
    REDDIT_ICON = "images/logo.png"
    st.image(REDDIT_ICON, width=100)
   
    st.title('FindAReddit Insights')
    
    df = sample_data()

    st.line_chart(df)

'''
    path = 'data/full_QA_pair.csv'
    df_QA = pd.read_csv(path)
    df_QA = df_QA.drop(columns=['comment_id','comment_upvotes','suggested_subreddits']).drop_duplicates()

    stop_words = set(STOPWORDS)

    fig, ax = plt.subplots()
    plt.figure(figsize = (20,6)) 
    wc = WordCloud(max_words = 1000 
              , width = 1600
              , height = 800
              , background_color ='white'
              , stopwords = set(stop_words)).generate(" ".join(df_QA.question_vocab)) 
    
    plt.imshow(wc , interpolation = 'bilinear')

    plt.show()
    st.pyplot(fig)

'''