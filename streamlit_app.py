import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

# Better way to read the key on Streamlit Cloud
CARDSIGHT_KEY = st.secrets.get("CARDSIGHT_API_KEY", "") or os.environ.get("CARDSIGHT_API_KEY", "")

# Debug line - add this temporarily so you can see if the key is loading
with st.sidebar:
    if CARDSIGHT_KEY:
        st.success("✅ Cardsight API key loaded successfully")
    else:
        st.warning("⚠️ No Cardsight API key detected — using fallback images")
