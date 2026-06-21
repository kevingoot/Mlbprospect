import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Prospect Scout", page_icon="⚾", layout="wide")

st.title("Prospect Scout")
st.caption("MLB Trade Show Tool - 2026 Prospects")

# Simple fresh data
data = [
    {"rank": 1, "player": "Jesús Made", "team": "MIL", "score": 92, "rec": "Strong Buy"},
    {"rank": 2, "player": "Colt Emerson", "team": "SEA", "score": 88, "rec": "Strong Buy"},
    {"rank": 3, "player": "Leo De Vries", "team": "OAK", "score": 85, "rec": "Buy/Hold"},
    {"rank": 4, "player": "Eli Willits", "team": "WSN", "score": 78, "rec": "Buy/Hold"},
    {"rank": 5, "player": "Max Clark", "team": "DET", "score": 82, "rec": "Strong Buy"},
    {"rank": 6, "player": "Franklin Arias", "team": "BOS", "score": 79, "rec": "Buy/Hold"},
]

df = pd.DataFrame(data)

with st.sidebar:
    if st.button("Refresh Data", type="primary"):
        st.cache_data.clear()
        st.success("Data refreshed")
    search = st.text_input("Search")

filtered = df.copy()
if search:
    filtered = filtered[filtered["player"].str.contains(search, case=False)]

st.subheader("Prospect List")
for _, row in filtered.iterrows():
    c1, c2, c3, c4 = st.columns([3, 1, 1, 2])
    with c1:
        st.write(f"**{row['player']}** ({row['team']})")
    with c2:
        st.metric("Score", row['score'])
    with c3:
        st.write(row['rec'])
    with c4:
        if st.button("Details", key=row['player']):
            st.session_state.current_player = row['player']

st.divider()

st.subheader("Full Spreadsheet")
for i, row in filtered.iterrows():
    c1, c2, c3, c4, c5 = st.columns([1, 3, 1, 1, 2])
    with c1:
        st.write(row['rank'])
    with c2:
        st.write(row['player'])
    with c3:
        st.write(row['team'])
    with c4:
        st.metric("Score", row['score'])
    with c5:
        if st.button("View", key=f"v{i}"):
            st.session_state.current_player = row['player']

# Detail View
if "current_player" in st.session_state:
    player = st.session_state.current_player
    st.divider()
    if st.button("Back to List"):
        st.session_state.current_player = None
        st.rerun()
    
    st.title(player)
    st.write("Call-up Score: **High**")
    st.header("Popular Cards")
    st.write("- Bowman Chrome Refractor: $25-$80")
    st.write("- Topps Auto: $80-$250")
    st.header("Upcoming Sets")
    st.link_button("Bowman Chrome", "https://amazon.com")
    st.link_button("Topps Update", "https://ebay.com")

st.success(f"Updated {datetime.now().strftime('%I:%M %p')}")
