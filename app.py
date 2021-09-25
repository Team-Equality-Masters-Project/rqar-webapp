import streamlit as st
from app_sidebar import QA_App
from apps import home, stats, kg

app = QA_App()

app.add_app("Home", home.app)
app.add_app("Subreddit Stats", stats.app)
app.add_app("Subreddit Graph", kg.app)

app.run()