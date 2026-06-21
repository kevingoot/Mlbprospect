import streamlit as st
from datetime import datetime

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

st.title("MLB Prospect Analyzer")
st.caption("Trade Show Edition • Tap team")

teams = [
    ("ARI", "#A71930", "Diamondbacks"), ("ATL", "#CE1141", "Braves"), ("BAL", "#DF4601", "Orioles"),
    ("BOS", "#BD3039", "Red Sox"), ("CHC", "#0E3386", "Cubs"), ("CHW", "#000000", "White Sox"),
    ("CIN", "#C6011F", "Reds"), ("CLE", "#E50022", "Guardians"), ("COL", "#33006F", "Rockies"),
    ("DET", "#0C2C56", "Tigers"), ("HOU", "#EB6E1F", "Astros"), ("KC", "#004874", "Royals"),
    ("LAA", "#BA002F", "Angels"), ("LAD", "#005A9C", "Dodgers"), ("MIA", "#00A3E0", "Marlins"),
    ("MIL", "#0A2E5A", "Brewers"), ("MIN", "#002B5C", "Twins"), ("NYM", "#FF5910", "Mets"),
    ("NYY", "#0C2C56", "Yankees"), ("OAK", "#003087", "Athletics"), ("PHI", "#E81828", "Phillies"),
    ("PIT", "#FDB827", "Pirates"), ("SD", "#2F3C4A", "Padres"), ("SF", "#FD5A1E", "Giants"),
    ("SEA", "#0C2C56", "Mariners"), ("STL", "#C41E3A", "Cardinals"), ("TB", "#8FBCE6", "Rays"),
    ("TEX", "#C0111F", "Rangers"), ("TOR", "#134A8E", "Blue Jays"), ("WSN", "#AB0003", "Nationals"),
]

if "current_team" not in st.session_state:
    st.session_state.current_team = None

if st.session_state.current_team is None:
    st.subheader("Select Team")
    cols = st.columns(3)
    for i, (code, color, name) in enumerate(teams):
        with cols[i % 3]:
            if st.button(f"{code} {name}", key=code, use_container_width=True):
                st.session_state.current_team = code
                st.rerun()
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
