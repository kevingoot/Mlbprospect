import streamlit as st
from datetime import datetime

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

st.markdown("""
<style>
    /* iOS color fixes */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton > button {
        background-color: #1e3a5f !important;
        color: #ffffff !important;
        border: 1px solid #4a90d9 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background-color: #2a5298 !important;
        border-color: #7ab3f0 !important;
    }
    .stButton > button:active {
        background-color: #4a90d9 !important;
    }
    div[data-testid="stSuccess"] {
        background-color: #1a3a1a !important;
        color: #4caf50 !important;
    }
    h1, h2, h3 {
        color: #ffffff !important;
    }
    .prospect-card {
        background-color: #1e2530;
        border: 1px solid #4a90d9;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .score-high { color: #4caf50; font-weight: bold; }
    .score-med  { color: #ff9800; font-weight: bold; }
    .score-low  { color: #f44336; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

teams = [
    ("ARI", "Diamondbacks"), ("ATL", "Braves"),    ("BAL", "Orioles"),
    ("BOS", "Red Sox"),      ("CHC", "Cubs"),       ("CHW", "White Sox"),
    ("CIN", "Reds"),         ("CLE", "Guardians"),  ("COL", "Rockies"),
    ("DET", "Tigers"),       ("HOU", "Astros"),     ("KC",  "Royals"),
    ("LAA", "Angels"),       ("LAD", "Dodgers"),    ("MIA", "Marlins"),
    ("MIL", "Brewers"),      ("MIN", "Twins"),      ("NYM", "Mets"),
    ("NYY", "Yankees"),      ("OAK", "Athletics"),  ("PHI", "Phillies"),
    ("PIT", "Pirates"),      ("SD",  "Padres"),     ("SF",  "Giants"),
    ("SEA", "Mariners"),     ("STL", "Cardinals"),  ("TB",  "Rays"),
    ("TEX", "Rangers"),      ("TOR", "Blue Jays"),  ("WSN", "Nationals"),
]

if "current_team" not in st.session_state:
    st.session_state.current_team = None
if "selected_player" not in st.session_state:
    st.session_state.selected_player = None

# ── TEAM SELECTION ──────────────────────────────────────────────────────────
if st.session_state.current_team is None:
    st.subheader("⚾ Select a Team")
    cols = st.columns(2)
    for i, (code, name) in enumerate(teams):
        with cols[i % 2]:
            if st.button(f"{code}  {name}", key=code, use_container_width=True):
                st.session_state.current_team = code
                st.session_state.selected_player = None
                st.rerun()

# ── TEAM PROSPECTS ───────────────────────────────────────────────────────────
else:
    team = st.session_state.current_team

    # Back button
    if st.button("← Back to Teams"):
        st.session_state.current_team = None
        st.session_state.selected_player = None
        st.rerun()

    st.title(f"⚾ {team} Top Prospects")

    # --- swap in real per-team data here as needed ---
    prospects = [
        {"player": "Jesús Made",   "pos": "SS", "score": 92,
         "bowman": "$25–80",  "topps": "$80–250",  "call_up": "High"},
        {"player": "Colt Emerson", "pos": "SS", "score": 88,
         "bowman": "$15–50",  "topps": "$60–180",  "call_up": "Medium"},
        {"player": "Leo De Vries", "pos": "SS", "score": 85,
         "bowman": "$10–40",  "topps": "$40–120",  "call_up": "Medium"},
    ]

    for p in prospects:
        label = f"{'🟢' if p['score'] >= 90 else '🟡' if p['score'] >= 85 else '🔴'}  {p['player']}  ({p['pos']})  —  Score: {p['score']}"
        if st.button(label, key=p["player"], use_container_width=True):
            if st.session_state.selected_player == p["player"]:
                st.session_state.selected_player = None   # toggle off
            else:
                st.session_state.selected_player = p["player"]
            st.rerun()

    # ── PLAYER DETAIL ────────────────────────────────────────────────────────
    if st.session_state.selected_player:
        match = next((p for p in prospects if p["player"] == st.session_state.selected_player), None)
        if match:
            st.divider()
            score_class = "score-high" if match["score"] >= 90 else "score-med" if match["score"] >= 85 else "score-low"
            st.markdown(f"""
<div class="prospect-card">
  <h2 style="color:#ffffff;margin-top:0">{match['player']}</h2>
  <p><b>Position:</b> {match['pos']}</p>
  <p><b>Call-up Score:</b> <span class="{score_class}">{match['score']} — {match['call_up']}</span></p>
  <hr style="border-color:#4a90d9"/>
  <p>🃏 <b>Bowman:</b> {match['bowman']}</p>
  <p>📦 <b>Topps:</b> {match['topps']}</p>
</div>
""", unsafe_allow_html=True)

            if st.button("✕  Close", key="close_player"):
                st.session_state.selected_player = None
                st.rerun()

st.success(f"Updated {datetime.now().strftime('%I:%M %p')}")
