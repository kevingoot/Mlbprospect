import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Prospect Spreadsheet", page_icon="⚾", layout="wide")

st.title("MLB Prospect Spreadsheet")
st.caption("Click View for player details")

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
st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
    column_config={
        "player": st.column_config.TextColumn("Player"),
        "score": st.column_config.NumberColumn("Call-up Score"),
    }
)

for i, row in filtered.iterrows():
    if st.button(f"View {row['player']}", key=f"v{i}"):
        st.session_state.selected = row['player']

if "selected" in st.session_state:
    player = st.session_state.selected
    st.divider()
    if st.button("Back"):
        st.session_state.selected = None
        st.rerun()
    st.title(player)
    st.write("Score: High")
    st.write("Cards: Bowman $25-80 | Topps $80-250")

st.success(f"Updated {datetime.now().strftime('%I:%M %p')}")
