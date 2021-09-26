import streamlit as st
from importlib.metadata import version


class QA_App:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):

        REDDIT_ICON = "images/logo.png"
        
        st.set_page_config(page_title="FindAReddit"
                           , page_icon=REDDIT_ICON
                           , layout="centered"
                           , initial_sidebar_state="expanded")

        st.sidebar.title("Navigation")
        
        
        app = st.sidebar.radio(
            'Go To',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()

        st.sidebar.header("About")
        st.sidebar.info(
            """
            This is a factoid based QA system focuses on answering a user’s query 
            about subreddit suggestions with a list of subreddits ranked by relevance. 
            This QA task combines multiple disciplines of machine learning such as 
            Information Retrieval (IR), Reinforcement Learning (RL), 
            Ranking and Recommendation (RR), and Knowledge Graph (KG).
            """ 
        )

        st.sidebar.markdown(
            f"""
            [![Streamlit](https://flat.badgen.net/badge/streamlit/
            {version('streamlit')}/grey?icon=pypi)]
            (https://github.com/streamlit/streamlit)
            """
        )