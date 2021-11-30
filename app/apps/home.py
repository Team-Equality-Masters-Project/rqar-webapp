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
    return card_html_code.format(img_url,  sub_url, sub_name, desc, subscriber_count, confidence, confidence,confidence,)

	
def make_info_tile(rl_text): 	
    info_html = open("resources/rl_info.html", 'r', encoding='utf-8')	
    info_html_code = info_html.read() 	
    return info_html_code.format(rl_text)

def app():
    REDDIT_ICON = "images/logo.png"
    
    with open('resources/style.css') as f:	
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)	
    

    st.image(REDDIT_ICON, width=100)
    st.title('Find A Reddit')

    st.write("A Reinforcement-based QA Recommender System for Responding to Community-based Suggestions using Enhanced Contextualization")
    with st.expander("Help text"):
        st.info(""":bulb: Please use the textbox to enter the question and submit it.""")
        st.info(""":bulb: In the question refinement section,
                click 'Yes' to accept question refinement, 'No' to find more refinements and 'Quit' to exit the refinement.""")
        st.info(""":bulb:You can view the suggested subreddits and a graph showing the relations between the suggested subreddits""")


    st.subheader("Tell us what subreddit you're looking for.")
    question = st.text_area("Provide your description", height = 150, max_chars=3000)
    rl_option = 'Adequacy'

    with st.expander("Set advanced environment options"):
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        rl_option = st.radio(label = 'What type of question improvement would you prefer?',
                             options = ['Adequacy','Fluency','Diversity', 'Best'])
        

    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    col1, col2, col3 = st.columns([1,1,1])
    clicked = col2.button("Find subreddit", key='submit') or st.session_state.clicked

    suggestions = {}
    rl_section = st.empty()

    if clicked:
        if len(question) == 0:
            st.error("Please provide your description")
        else:
            st.session_state.clicked = True
            with rl_section.container():
                rl_text_col, yes_btn_col, no_btn_col, q_btn_col = st.columns((8,1,1,1))
                rl_text, event_id = rl_api.get_rl_text(question, rl_option)
                rl_text_col.markdown(make_info_tile(rl_text), unsafe_allow_html=True)
                yes_btn = yes_btn_col.button("Yes", 'y')
                no_btn = no_btn_col.button("No", 'n')
                q_btn = q_btn_col.button("Quit", 'q')
            
            count = 0
            while no_btn:
                rl_api.update_model(yes_btn, no_btn, event_id)
                rl_section.empty()
                with rl_section.container():
                    rl_text_col, yes_btn_col, no_btn_col, q_btn_col = st.columns((8,1,1,1))
                    rl_text, event_id = rl_api.get_rl_text(question, rl_option)
                    rl_text_col.markdown(make_info_tile(rl_text), unsafe_allow_html=True)
                    yes_btn = yes_btn_col.button("Yes", 'y'+str(count))
                    no_btn = no_btn_col.button("No", 'n'+str(count))
                    q_btn = q_btn_col.button("Quit", 'q'+str(count))
                count = count+2

            if yes_btn or q_btn:
                rl_section.empty()
                if yes_btn:
                    question = rl_text
                    with st.spinner(":hourglass_flowing_sand: Updating RL model..."):
                        rl_api.update_model(yes_btn, no_btn, event_id)
                        
                with st.spinner(":hourglass_flowing_sand: Retrieving subreddits and ranking..."):
                    suggestions = model.RQAR(question)
                with st.spinner(":heavy_check_mark: Fetched subreddits!"):
                    col1, col2, col3 = st.columns(3)
                    try:
                        col1.markdown(make_sub_tile(suggestions[0][0], suggestions[0][1]), unsafe_allow_html=True)
                        col2.markdown(make_sub_tile(suggestions[1][0], suggestions[1][1]), unsafe_allow_html=True)
                        col3.markdown(make_sub_tile(suggestions[2][0], suggestions[2][1]), unsafe_allow_html=True)
                        col1.markdown(make_sub_tile(suggestions[3][0], suggestions[3][1]), unsafe_allow_html=True)
                        col2.markdown(make_sub_tile(suggestions[4][0], suggestions[4][1]), unsafe_allow_html=True)
                        col3.markdown(make_sub_tile(suggestions[5][0], suggestions[5][1]), unsafe_allow_html=True)
                    except:
                        st.error("Reddit API limit reached!")

                    st.markdown("### Knowledge graph")  

                    G = nx.read_gpickle("data/kg-large.gpickle")
                    g = G.subgraph([ sug[0] for sug in suggestions])
                    sub_graph = Network(width='100%')
                    sub_graph.from_nx(g)
                    sub_graph.show('resources/subgraph.html')
                    subgraph_html = open("resources/subgraph.html", 'r', encoding='utf-8')
                    subgraph_html_code = subgraph_html.read() 
                    components.html(subgraph_html_code, height=600)
                    

                
                
