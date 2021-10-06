import base64
import time

import data.reddit_api as reddit_api
import data.rl_api as rl_api
import data.RQAR as model
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from IPython.core.display import HTML, display
from pyvis.network import Network


def make_sub_tile(sub_name, confidence): 
    card_html = open("resources/card.html", 'r', encoding='utf-8')
    card_html_code = card_html.read() 
    img_url, sub_name, desc, sub_url, banner_img_url, subscriber_count, created_time = reddit_api.get_details(sub_name)
    return card_html_code.format(img_url, sub_url, sub_name, desc, subscriber_count)

	
def make_info_tile(question): 	
    info_html = open("resources/rl_info.html", 'r', encoding='utf-8')	
    info_html_code = info_html.read() 	
    rl_text = rl_api.get_rl_text(question)	
    return info_html_code.format(rl_text)

def app():
    REDDIT_ICON = "images/logo.png"
    
    with open('resources/style.css') as f:	
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)	
    

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

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    col1, col2, col3 = st.columns([1,1,1])
    clicked = col2.button("Find subreddit") or st.session_state.clicked

    suggestions = {}
    rl_section = st.empty()

    if clicked:
        if len(question) == 0:
            st.error("Please provide your description")
        else:
            st.session_state.clicked = True
            with rl_section.container():
                rl_text_col, yes_btn_col, no_btn_col = st.columns((8,1,1))
                rl_text_col.markdown(make_info_tile(question),unsafe_allow_html=True)
                
                '''st.markdown("""
                    <style>
                    div.stButton > button:first-child {
                        background-color: #eee;
                    }
                    </style>""", unsafe_allow_html=True)'''
                yes_btn = yes_btn_col.button("Yes")
                no_btn = no_btn_col.button("No")
            

            if yes_btn or no_btn:
                rl_section.empty()
            
                with st.spinner(":hourglass_flowing_sand: Updating RL model..."):
                    time.sleep(1)
                    rl_api.update_model(yes_btn, no_btn)
                with st.spinner(":hourglass_flowing_sand: Retrieving subreddits and ranking..."):
                    time.sleep(1)
                with st.spinner(":heavy_check_mark: Fetched subreddits!"):
                    time.sleep(1)
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
                sub_graph.show('resources/subgraph.html')
                subgraph_html = open("resources/subgraph.html", 'r', encoding='utf-8')
                subgraph_html_code = subgraph_html.read() 
                components.html(subgraph_html_code, height=600)

    
    


