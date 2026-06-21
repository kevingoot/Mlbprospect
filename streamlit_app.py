import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

st.title("MLB Prospect Analyzer")
st.caption("Trade Show Edition • Tap a team")

teams = ["MIL", "SEA", "OAK", "WSN", "DET", "BOS", "CLE", "PIT", "SD", "NYM", "NYY", "LAD", "HOU", "PHI", "ATL"]

if "current_team" not in st.session_state:
    st.session_state.current_team = None

if st.session_state.current_team is None:
    st.subheader("Select Team")
    cols = st.columns(5)
    for i, team in enumerate(teams):
        with cols[i % 5]:
            if st.button(team, key=team, use_container_width=True):
                st.session_state.current_team = team
                st.rerun()
else:
    team = st.session_state.current_team
    if st.button("← Back to Teams"):
        st.session_state.current_team = None
        st.rerun()
    
    st.title(f"{team} Top 10 Prospects")
    
    # Example prospects
    prospects = [
        {"player": "Jesús Made", "pos": "SS", "score": 92},
        {"player": "Colt Emerson", "pos": "SS", "score": 88},
        {"player": "Leo De Vries", "pos": "SS", "score": 85},
    ]
    
    for p in prospects:
        if st.button(f"{p['player']} ({p['pos']}) - Score: {p['score']}", key=p['player']):
            st.session_state.selected_player = p['player']
    
    if "selected_player" in st.session_state:
        player = st.session_state.selected_player
        st.divider()
        st.header(player)
        st.write("Call-up Score: High")
        st.write("Cards: Bowman $25-80 | Topps $80-250")
        if st.button("Close"):
            st.session_state.selected_player = None
            st.rerun()

st.success(f"Updated {datetime.now().strftime('%I:%M %p')}")
