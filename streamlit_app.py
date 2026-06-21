import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Prospect Spreadsheet", page_icon="⚾", layout="wide")

st.title("MLB Prospect Spreadsheet")
st.caption("Click any row for details • Trade Show Ready")

# Data
data = [
    {"rank": 1, "player": "Jesús Made", "team": "MIL", "score": 92, "rec": "Strong Buy"},
    {"rank": 2, "player": "Colt Emerson", "team": "SEA", "score": 88, "rec": "Strong Buy"},
    {"rank": 3, "player": "Leo De Vries", "team": "OAK", "score": 85, "rec": "Buy/Hold"},
    {"rank": 4, "player": "Eli Willits", "team": "WSN", "score": 78, "rec": "Buy/Hold"},
    {"rank": 5, "player": "Max Clark", "team": "DET", "score": 82, "rec": "Strong Buy"},
    {"rank": 6, "player": "Franklin Arias", "team": "BOS", "score": 79, "rec": "Buy/Hold"},
]

df = pd.DataFrame(data)

search = st.text_input("Search Player")

filtered = df
if search:
    filtered = df[df["player"].str.contains(search, case=False)]

# The Spreadsheet
st.subheader("Prospects")
for i, row in filtered.iterrows():
    cols = st.columns([1, 4, 1, 1, 2])
    with cols[0]:
        st.write(row['rank'])
    with cols[1]:
        st.write(row['player'])
    with cols[2]:
        st.write(row['team'])
    with cols[3]:
        st.metric("Score", row['score'])
    with cols[4]:
        if st.button("View Details", key=f"v{i}"):
            st.session_state.selected = row['player']

# Detail View
if "selected" in st.session_state:
    player = st.session_state.selected
    st.divider()
    if st.button("← Back to Spreadsheet"):
        st.session_state.selected = None
        st.rerun()
    
    st.title(player)
    st.write("Call-up Score: High")
    st.header("Popular Cards")
    st.write("Bowman Chrome Refractor: $25-$80")
    st.write("Topps Auto: $80-$250")
    st.header("Upcoming Sets")
    st.link_button("Bowman Chrome", "https://amazon.com")
    st.link_button("Topps Update", "https://ebay.com")

st.success(f"Updated {datetime.now().strftime('%I:%M %p')}")
