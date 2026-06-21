import streamlit as st
from datetime import datetime

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

st.title("MLB Prospect Analyzer")
st.caption("Trade Show Edition • Tap team")

teams = [
    ("MIL", "#0A2E5A", "Brewers"),
    ("SEA", "#0C2C56", "Mariners"),
    ("OAK", "#003087", "Athletics"),
    ("WSN", "#AB0003", "Nationals"),
    ("DET", "#0C2C56", "Tigers"),
    ("BOS", "#BD3039", "Red Sox"),
    ("CLE", "#E50022", "Guardians"),
    ("PIT", "#FDB827", "Pirates"),
    ("SD", "#2F3C4A", "Padres"),
    ("NYM", "#FF5910", "Mets"),
]

if "current_team" not in st.session_state:
    st.session_state.current_team = None

if st.session_state.current_team is None:
    st.subheader("Select Team")
    for code, color, name in teams:
        st.markdown(f"""
        <a href="#" onclick="window.location.href='?team={code}'" style="background-color:{color}; color:white; padding:10px; border-radius:8px; display:block; margin:5px; text-align:center; text-decoration:none;">
            {code} {name}
        </a>
        """, unsafe_allow_html=True)
else:
    team = st.session_state.current_team
    if st.button("← Back to Teams"):
        st.session_state.current_team = None
        st.rerun()
    
    st.title(f"{team} Top Prospects")
    
    prospects = [
        {"player": "Jesús Made", "pos": "SS", "score": 92},
        {"player": "Colt Emerson", "pos": "SS", "score": 88},
        {"player": "Leo De Vries", "pos": "SS", "score": 85},
    ]
    
    for p in prospects:
        if st.button(f"{p['player']} ({p['pos']}) - {p['score']}", key=p['player']):
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
