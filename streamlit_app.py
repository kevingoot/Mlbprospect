import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

# ── STYLING ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background: #0d1117 !important; }
    h1, h2, h3 { color: #ffffff !important; }
    .stButton > button {
        background: #1c2a3e !important;
        color: #79c0ff !important;
        border: 1px solid #30475e !important;
        border-radius: 8px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 12px 10px !important;
        height: 68px !important;
        line-height: 1.3 !important;
        text-align: center !important;
        white-space: pre-wrap !important;
    }
    .stSuccess {
        background: #0d2818 !important;
        color: #3fb950 !important;
        border: 1px solid #238636 !important;
    }
</style>
""", unsafe_allow_html=True)

TEAMS = [
    ("ARI","Diamondbacks"), ("ATL","Braves"),    ("BAL","Orioles"),
    ("BOS","Red Sox"),      ("CHC","Cubs"),       ("CHW","White Sox"),
    ("CIN","Reds"),         ("CLE","Guardians"),  ("COL","Rockies"),
    ("DET","Tigers"),       ("HOU","Astros"),     ("KC", "Royals"),
    ("LAA","Angels"),       ("LAD","Dodgers"),    ("MIA","Marlins"),
    ("MIL","Brewers"),      ("MIN","Twins"),      ("NYM","Mets"),
    ("NYY","Yankees"),      ("OAK","Athletics"),  ("PHI","Phillies"),
    ("PIT","Pirates"),      ("SD", "Padres"),     ("SF", "Giants"),
    ("SEA","Mariners"),     ("STL","Cardinals"),  ("TB", "Rays"),
    ("TEX","Rangers"),      ("TOR","Blue Jays"),  ("WSN","Nationals"),
]

PROSPECTS = {
    "ARI": [{"player":"Cristian Mena","pos":"RHP","score":88,"call_up":"High","bowman":"$20-60","topps":"$60-180"}],
    "ATL": [{"player":"Hurston Waldrep","pos":"RHP","score":87,"call_up":"High","bowman":"$15-50","topps":"$50-150"}],
    "BAL": [{"player":"Jackson Holliday","pos":"SS","score":93,"call_up":"High","bowman":"$40-120","topps":"$120-350"}],
    "BOS": [{"player":"Roman Anthony","pos":"OF","score":95,"call_up":"High","bowman":"$60-200","topps":"$200-600"}],
    "CHC": [{"player":"Matt Shaw","pos":"SS","score":85,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"}],
    "CHW": [{"player":"Colson Montgomery","pos":"SS","score":87,"call_up":"High","bowman":"$20-65","topps":"$65-190"}],
    "CIN": [{"player":"Rhett Lowder","pos":"RHP","score":88,"call_up":"High","bowman":"$20-65","topps":"$65-200"}],
    "CLE": [{"player":"Gavin Williams","pos":"RHP","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"}],
    "COL": [{"player":"Chase Dollander","pos":"RHP","score":90,"call_up":"High","bowman":"$30-90","topps":"$90-270"}],
    "DET": [{"player":"Jackson Jobe","pos":"RHP","score":91,"call_up":"High","bowman":"$35-110","topps":"$110-320"}],
    "HOU": [{"player":"Brice Matthews","pos":"SS","score":84,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"}],
    "KC": [{"player":"Jac Caglianone","pos":"1B/LHP","score":90,"call_up":"High","bowman":"$30-90","topps":"$90-270"}],
    "LAA": [{"player":"Nolan Schanuel","pos":"1B","score":85,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"}],
    "LAD": [{"player":"Dalton Rushing","pos":"C","score":89,"call_up":"High","bowman":"$25-80","topps":"$80-230"}],
    "MIA": [{"player":"Noble Meyer","pos":"RHP","score":91,"call_up":"High","bowman":"$35-110","topps":"$110-320"}],
    "MIL": [{"player":"Jackson Chourio","pos":"OF","score":88,"call_up":"High","bowman":"$25-80","topps":"$80-230"}],
    "MIN": [{"player":"Walker Jenkins","pos":"OF","score":93,"call_up":"High","bowman":"$45-140","topps":"$140-420"}],
    "NYM": [{"player":"Kevin Parada","pos":"C","score":88,"call_up":"High","bowman":"$20-65","topps":"$65-200"}],
    "NYY": [{"player":"Jasson Dominguez","pos":"OF","score":90,"call_up":"High","bowman":"$30-90","topps":"$90-270"}],
    "OAK": [{"player":"Lawrence Butler","pos":"OF","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"}],
    "PHI": [{"player":"Andrew Painter","pos":"RHP","score":90,"call_up":"High","bowman":"$30-90","topps":"$90-270"}],
    "PIT": [{"player":"Paul Skenes","pos":"RHP","score":98,"call_up":"High","bowman":"$100-350","topps":"$350-1000"}],
    "SD": [{"player":"Ethan Salas","pos":"C","score":93,"call_up":"High","bowman":"$45-140","topps":"$140-420"}],
    "SF": [{"player":"Bryce Eldridge","pos":"1B/RHP","score":89,"call_up":"High","bowman":"$25-80","topps":"$80-230"}],
    "SEA": [{"player":"Colt Emerson","pos":"SS","score":88,"call_up":"High","bowman":"$25-80","topps":"$80-250"}],
    "STL": [{"player":"Masyn Winn","pos":"SS","score":88,"call_up":"High","bowman":"$20-65","topps":"$65-200"}],
    "TB": [{"player":"Carson Williams","pos":"SS","score":90,"call_up":"High","bowman":"$30-90","topps":"$90-270"}],
    "TEX": [{"player":"Wyatt Langford","pos":"OF","score":89,"call_up":"High","bowman":"$25-80","topps":"$80-230"}],
    "TOR": [{"player":"Ricky Tiedemann","pos":"LHP","score":91,"call_up":"High","bowman":"$35-110","topps":"$110-320"}],
    "WSN": [{"player":"James Wood","pos":"OF","score":96,"call_up":"High","bowman":"$80-250","topps":"$250-750"}],
}

if "current_team" not in st.session_state:
    st.session_state.current_team = None
if "selected_player" not in st.session_state:
    st.session_state.selected_player = None

# ── TEAM SELECTION ──────────────────────────────────────────────────────────
if st.session_state.current_team is None:
    st.markdown("## ⚾ MLB Prospect Analyzer")
    st.markdown("*Trade Show Edition — Tap a team*")

    cols = st.columns(3)
    for i, (code, name) in enumerate(TEAMS):
        with cols[i % 3]:
            if st.button(f"{code}\n{name}", key=f"team_{code}", use_container_width=True):
                st.session_state.current_team = code
                st.session_state.selected_player = None
                st.rerun()

# ── TEAM PROSPECTS ──────────────────────────────────────────────────────────
else:
    team = st.session_state.current_team
    team_name = next(n for c, n in TEAMS if c == team)

    if st.button("← Back to All Teams"):
        st.session_state.current_team = None
        st.session_state.selected_player = None
        st.rerun()

    st.markdown(f"### {team} — Top Prospects")

    prospects = PROSPECTS.get(team, [])

    for p in prospects:
        if st.button(f"{p['player']} ({p['pos']}) — Score: {p['score']}", key=f"p_{p['player']}", use_container_width=True):
            st.session_state.selected_player = None if st.session_state.selected_player == p["player"] else p["player"]
            st.rerun()

        if st.session_state.selected_player == p["player"]:
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid #58a6ff;border-radius:10px;padding:16px 20px;margin:8px 0 16px 0;">
                <div style="color:#ffffff;font-size:20px;font-weight:700;">{p['player']} <span style="color:#58a6ff;">{p['pos']}</span></div>
                <div style="display:flex;justify-content:space-between;margin-top:12px;">
                    <div><span style="color:#8b949e;">CALL-UP</span><br><span style="color:#3fb950;font-size:28px;font-weight:700;">{p['score']}</span></div>
                    <div><span style="color:#8b949e;">Bowman</span><br><span style="color:#79c0ff;font-weight:600;">{p['bowman']}</span></div>
                    <div><span style="color:#8b949e;">Topps</span><br><span style="color:#79c0ff;font-weight:600;">{p['topps']}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Close", key=f"close_{p['player']}"):
                st.session_state.selected_player = None
                st.rerun()

st.success(f"Updated {datetime.now().strftime('%I:%M %p')}")
