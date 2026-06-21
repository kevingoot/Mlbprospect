import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Prospect Spreadsheet", page_icon="⚾", layout="wide")

st.title("MLB Prospect Spreadsheet")
st.caption("Tap player name for details")

data = [
    {"rank": 1, "player": "Jesús Made", "team": "MIL", "score": 92, "rec": "Strong Buy"},
    {"rank": 2, "player": "Colt Emerson", "team": "SEA", "score": 88, "rec": "Strong Buy"},
    {"rank": 3, "player": "Leo De Vries", "team": "OAK", "score": 85, "rec": "Buy/Hold"},
    {"rank": 4, "player": "Eli Willits", "team": "WSN", "score": 78, "rec": "Buy/Hold"},
    {"rank": 5, "player": "Max Clark", "team": "DET", "score": 82, "rec": "Strong Buy"},
    {"rank": 6, "player": "Franklin Arias", "team": "BOS", "score": 79, "rec": "Buy/Hold"},
]

df = pd.DataFrame(data)

search = st.text_input("Search")

filtered = df
if search:
    filtered = df[df["player"].str.contains(search, case=False)]

st.subheader("Prospect Spreadsheet")
for i, row in filtered.iterrows():
    cols = st.columns([1, 4, 1, 1, 2])
    with cols[0]:
        st.write(row['rank'])
    with cols[1]:
        if st.button(row['player'], key=f"name_{i}"):
            st.session_state.selected = row['player']
    with cols[2]:
        st.write(row['team'])
    with cols[3]:
        st.metric("Score", row['score'])
    with cols[4]:
        st.write(row['rec'])

# Detail
if "selected" in st.session_state:
    player = st.session_state.selected
    st.divider()
    if st.button("Back to Spreadsheet"):
        st.session_state.selected = None
        st.rerun()
    st.title(player)
    st.write("Score: High")
    st.write("Cards: Bowman $25-80 | Topps $80-250")
    st.header("Upcoming Sets")
    st.link_button("Bowman Chrome", "https://amazon.com")

st.success(f"Updated {datetime.now().strftime('%I:%M %p')}")
