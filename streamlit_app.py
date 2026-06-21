import streamlit as st
from datetime import datetime

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

st.title("MLB Prospect Analyzer")
st.caption("Trade Show Edition • Tap team")

teams = [
    ("ARI", "Diamondbacks"), ("ATL", "Braves"), ("BAL", "Orioles"),
    ("BOS", "Red Sox"), ("CHC", "Cubs"), ("CHW", "White Sox"),
    ("CIN", "Reds"), ("CLE", "Guardians"), ("COL", "Rockies"),
    ("DET", "Tigers"), ("HOU", "Astros"), ("KC", "Royals"),
    ("LAA", "Angels"), ("LAD", "Dodgers"), ("MIA", "Marlins"),
    ("MIL", "Brewers"), ("MIN", "Twins"), ("NYM", "Mets"),
    ("NYY", "Yankees"), ("OAK", "Athletics"), ("PHI", "Phillies"),
    ("PIT", "Pirates"), ("SD", "Padres"), ("SF", "Giants"),
    ("SEA", "Mariners"), ("STL", "Cardinals"), ("TB", "Rays"),
    ("TEX", "Rangers"), ("TOR", "Blue Jays"), ("WSN", "Nationals"),
]

if "current_team" not in st.session_state:
    st.session_state.current_team = None

if st.session_state.current_team is None:
    st.subheader("Select Team")
    cols = st.columns(3)
    for i, (code, name) in enumerate(teams):
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
