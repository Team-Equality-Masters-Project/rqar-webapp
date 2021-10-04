import streamlit as st
import pandas as pd
import numpy as np
import time
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from IPython.core.display import display, HTML
import streamlit.components.v1 as components
import base64
# import data.model_api as model
import data.RQAR as model
import data.reddit_api as reddit_api


def make_sub_tile(sub_name, confidence): 
    card_html = open("resources/card.html", 'r', encoding='utf-8')
    card_html_code = card_html.read() 
    img_url, sub_name, desc, sub_url, banner_img_url, subscriber_count, created_time = reddit_api.get_details(sub_name)
    return card_html_code.format(img_url, sub_url, sub_name, desc, subscriber_count)


def app():
    REDDIT_ICON = "images/logo.png"
    st.image(REDDIT_ICON, width=100)
    st.title('Find A Reddit')

    st.write("A Reinforcement-based QA Recommender System for Responding to Community-based Suggestions using Enhanced Contextualization")
    with st.expander("Help text"):
        st.info(""":bulb:                  """)


    st.subheader("Tell us what subreddit you're looking for.")
    question = st.text_area("Provide your description", height = 150, max_chars=3000)

    with st.expander("Set advanced RL environment options"):
        st.number_input(
                    "Number 1",
                    step=1,
                    value=100,
                    help='Number1',
                )
        st.number_input(
                    "Number 2",
                    step=1,
                    value=100,
                    help='Number2',
                )

    clicked = st.button("Find subreddit")
    status = st.empty()
    suggestions = {}

    if clicked:
        with st.spinner(":hourglass_flowing_sand: Retrieving subreddits..."):
            time.sleep(1)
        with st.spinner(":hourglass_flowing_sand: Ranking..."):
            time.sleep(1)
        with st.spinner(":heavy_check_mark: Fetched subreddits!"):
            time.sleep(1)
            #suggestions = model.find_subreddits(question)
            suggestions = model.RQAR(question)

        
        col1, col2, col3 = st.columns(3)
        
        col1.markdown(make_sub_tile(suggestions[0][0], suggestions[0][1]), unsafe_allow_html=True)
        col2.markdown(make_sub_tile(suggestions[1][0], suggestions[1][1]), unsafe_allow_html=True)
        col3.markdown(make_sub_tile(suggestions[2][0], suggestions[2][1]), unsafe_allow_html=True)
        col1.markdown(make_sub_tile(suggestions[3][0], suggestions[3][1]), unsafe_allow_html=True)
        col2.markdown(make_sub_tile(suggestions[4][0], suggestions[4][1]), unsafe_allow_html=True)
        col3.markdown(make_sub_tile(suggestions[5][0], suggestions[5][1]), unsafe_allow_html=True)
        
        st.markdown("### Knowledge graph")  #(To change)

        G = nx.karate_club_graph()
        sub_graph = Network(width='100%')
        sub_graph.from_nx(G)
        sub_graph.show('subgraph.html')
        subgraph_html = open("subgraph.html", 'r', encoding='utf-8')
        subgraph_html_code = subgraph_html.read() 
        components.html(subgraph_html_code, height=600)

    
    


