import streamlit as st
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from IPython.core.display import display, HTML
import streamlit.components.v1 as components

def app():
    REDDIT_ICON = "images/logo.png"
    st.image(REDDIT_ICON, width=100)
   
    st.title('Subreddit Knowledge Graph')

    G = nx.read_gpickle("data/kg.gpickle")

    g4 = Network(height='800px', width='100%')

    g4.from_nx(G)

    #g4.show_buttons(filter_=['physics'])

    g4.show('resources/kg.html')
    
    kg_html = open("resources/kg.html", 'r', encoding='utf-8')
    kg_html_code = kg_html.read() 
    components.html(kg_html_code, height=1200)