import streamlit as st
from datetime import datetime

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0d1117 !important; }
[data-testid="stHeader"] { background: #0d1117 !important; }
section[data-testid="stMain"] { background: #0d1117 !important; }
.block-container { padding: 1rem !important; max-width: 100% !important; }
h1, h2, h3, h4 { color: #ffffff !important; }
p { color: #e6edf3 !important; }
.stButton > button {
    background: #1c2a3e !important;
    color: #79c0ff !important;
    border: 1px solid #30475e !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 0.5rem 0.75rem !important;
    width: 100% !important;
    text-align: left !important;
}
[data-testid="stSuccess"] > div {
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

TEAM_COLORS = {
    "ARI":"#A71930","ATL":"#CE1141","BAL":"#DF4601","BOS":"#BD3039",
    "CHC":"#0E3386","CHW":"#3D3D3D","CIN":"#C6011F","CLE":"#E31937",
    "COL":"#33006F","DET":"#0C2340","HOU":"#EB6E1F","KC":"#004687",
    "LAA":"#BA0021","LAD":"#005A9C","MIA":"#00A3E0","MIL":"#12284B",
    "MIN":"#002B5C","NYM":"#002D72","NYY":"#003087","OAK":"#003831",
    "PHI":"#E81828","PIT":"#FDB827","SD":"#4A3728","SF":"#FD5A1E",
    "SEA":"#0C2C56","STL":"#C41E3A","TB":"#092C5C","TEX":"#003278",
    "TOR":"#134A8E","WSN":"#AB0003",
}

PROSPECTS = {
    "ARI":[{"player":"Cristian Mena","pos":"RHP","score":88,"call_up":"High","bowman":"$20-60","topps":"$60-180"},
           {"player":"Deyvison De Los Santos","pos":"3B","score":85,"call_up":"Medium","bowman":"$15-45","topps":"$45-130"},
           {"player":"Jordan Lawlar","pos":"SS","score":82,"call_up":"Medium","bowman":"$10-35","topps":"$35-100"}],
    "ATL":[{"player":"Hurston Waldrep","pos":"RHP","score":87,"call_up":"High","bowman":"$15-50","topps":"$50-150"},
           {"player":"Drake Baldwin","pos":"C","score":83,"call_up":"Medium","bowman":"$10-35","topps":"$30-90"},
           {"player":"Nacho Alvarez Jr.","pos":"SS","score":80,"call_up":"Low","bowman":"$8-25","topps":"$25-70"}],
    "BAL":[{"player":"Jackson Holliday","pos":"SS","score":93,"call_up":"High","bowman":"$40-120","topps":"$120-350"},
           {"player":"Samuel Basallo","pos":"C","score":89,"call_up":"High","bowman":"$25-80","topps":"$80-230"},
           {"player":"Coby Mayo","pos":"3B","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"}],
    "BOS":[{"player":"Roman Anthony","pos":"OF","score":95,"call_up":"High","bowman":"$60-200","topps":"$200-600"},
           {"player":"Marcelo Mayer","pos":"SS","score":91,"call_up":"High","bowman":"$35-110","topps":"$110-320"},
           {"player":"Kyle Teel","pos":"C","score":87,"call_up":"High","bowman":"$20-65","topps":"$65-200"}],
    "CHC":[{"player":"Matt Shaw","pos":"SS","score":85,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"},
           {"player":"Kevin Made","pos":"SS","score":82,"call_up":"Medium","bowman":"$10-35","topps":"$30-90"},
           {"player":"Owen Caissie","pos":"OF","score":81,"call_up":"Low","bowman":"$8-30","topps":"$25-80"}],
    "CHW":[{"player":"Colson Montgomery","pos":"SS","score":87,"call_up":"High","bowman":"$20-65","topps":"$65-190"},
           {"player":"Noah Schultz","pos":"LHP","score":85,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"},
           {"player":"Cam Caminiti","pos":"SS","score":83,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"}],
    "CIN":[{"player":"Rhett Lowder","pos":"RHP","score":88,"call_up":"High","bowman":"$20-65","topps":"$65-200"},
           {"player":"Cam Collier","pos":"3B","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"},
           {"player":"Sal Stewart","pos":"3B","score":83,"call_up":"Medium","bowman":"$10-35","topps":"$35-100"}],
    "CLE":[{"player":"Gavin Williams","pos":"RHP","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"},
           {"player":"Chase DeLauter","pos":"OF","score":83,"call_up":"Medium","bowman":"$10-35","topps":"$30-90"},
           {"player":"Tanner Burns","pos":"RHP","score":80,"call_up":"Low","bowman":"$8-25","topps":"$20-60"}],
    "COL":[{"player":"Chase Dollander","pos":"RHP","score":90,"call_up":"High","bowman":"$30-90","topps":"$90-270"},
           {"player":"Adael Amador","pos":"SS","score":84,"call_up":"Medium","bowman":"$12-40","topps":"$35-100"},
           {"player":"Kyle Freeland Jr.","pos":"LHP","score":82,"call_up":"Medium","bowman":"$8-30","topps":"$25-75"}],
    "DET":[{"player":"Jackson Jobe","pos":"RHP","score":91,"call_up":"High","bowman":"$35-110","topps":"$110-320"},
           {"player":"Colt Keith","pos":"2B","score":87,"call_up":"High","bowman":"$20-65","topps":"$65-190"},
           {"player":"Ty Madden","pos":"RHP","score":82,"call_up":"Medium","bowman":"$8-30","topps":"$25-80"}],
    "HOU":[{"player":"Brice Matthews","pos":"SS","score":84,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"},
           {"player":"Chayce McDermott","pos":"RHP","score":83,"call_up":"Medium","bowman":"$10-35","topps":"$30-90"},
           {"player":"Colin Barber","pos":"OF","score":81,"call_up":"Low","bowman":"$8-25","topps":"$20-60"}],
    "KC": [{"player":"Jac Caglianone","pos":"1B/LHP","score":90,"call_up":"High","bowman":"$30-90","topps":"$90-270"},
           {"player":"Blake Mitchell","pos":"SS","score":87,"call_up":"High","bowman":"$20-65","topps":"$65-190"},
           {"player":"Gavin Cross","pos":"OF","score":85,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"}],
    "LAA":[{"player":"Nolan Schanuel","pos":"1B","score":85,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"},
           {"player":"Werner Blakely","pos":"SS","score":84,"call_up":"Medium","bowman":"$12-40","topps":"$35-105"},
           {"player":"Caden Dana","pos":"RHP","score":83,"call_up":"Medium","bowman":"$10-35","topps":"$30-90"}],
    "LAD":[{"player":"Dalton Rushing","pos":"C","score":89,"call_up":"High","bowman":"$25-80","topps":"$80-230"},
           {"player":"Nick Frasso","pos":"RHP","score":84,"call_up":"Medium","bowman":"$10-35","topps":"$30-90"},
           {"player":"Tommy Edman","pos":"SS","score":85,"call_up":"Medium","bowman":"$10-35","topps":"$35-100"}],
    "MIA":[{"player":"Noble Meyer","pos":"RHP","score":91,"call_up":"High","bowman":"$35-110","topps":"$110-320"},
           {"player":"Jacob Berry","pos":"3B","score":85,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"},
           {"player":"Karson Ligon","pos":"RHP","score":82,"call_up":"Medium","bowman":"$8-30","topps":"$25-80"}],
    "MIL":[{"player":"Jackson Chourio","pos":"OF","score":88,"call_up":"High","bowman":"$25-80","topps":"$80-230"},
           {"player":"Sal Frelick","pos":"OF","score":85,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"},
           {"player":"Joey Wiemer","pos":"OF","score":82,"call_up":"Medium","bowman":"$8-30","topps":"$25-80"}],
    "MIN":[{"player":"Walker Jenkins","pos":"OF","score":93,"call_up":"High","bowman":"$45-140","topps":"$140-420"},
           {"player":"Emmanuel Rodriguez","pos":"OF","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"},
           {"player":"Hurston Waldrep","pos":"RHP","score":84,"call_up":"Medium","bowman":"$10-35","topps":"$35-100"}],
    "NYM":[{"player":"Kevin Parada","pos":"C","score":88,"call_up":"High","bowman":"$20-65","topps":"$65-200"},
           {"player":"Jett Williams","pos":"SS","score":87,"call_up":"High","bowman":"$20-65","topps":"$65-190"},
           {"player":"Luisangel Acuna","pos":"SS","score":85,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"}],
    "NYY":[{"player":"Jasson Dominguez","pos":"OF","score":90,"call_up":"High","bowman":"$30-90","topps":"$90-270"},
           {"player":"Spencer Jones","pos":"OF","score":87,"call_up":"High","bowman":"$20-65","topps":"$65-190"},
           {"player":"George Lombard Jr.","pos":"OF","score":84,"call_up":"Medium","bowman":"$10-35","topps":"$35-100"}],
    "OAK":[{"player":"Lawrence Butler","pos":"OF","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"},
           {"player":"Zack Gelof","pos":"2B","score":85,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"},
           {"player":"Max Muncy","pos":"SS","score":83,"call_up":"Medium","bowman":"$10-35","topps":"$30-90"}],
    "PHI":[{"player":"Andrew Painter","pos":"RHP","score":90,"call_up":"High","bowman":"$30-90","topps":"$90-270"},
           {"player":"Aidan Miller","pos":"SS","score":88,"call_up":"High","bowman":"$20-65","topps":"$65-200"},
           {"player":"Mick Abel","pos":"RHP","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"}],
    "PIT":[{"player":"Paul Skenes","pos":"RHP","score":98,"call_up":"High","bowman":"$100-350","topps":"$350-1000"},
           {"player":"Termarr Johnson","pos":"2B","score":87,"call_up":"High","bowman":"$20-65","topps":"$65-190"},
           {"player":"Endy Rodriguez","pos":"C","score":85,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"}],
    "SD": [{"player":"Ethan Salas","pos":"C","score":93,"call_up":"High","bowman":"$45-140","topps":"$140-420"},
           {"player":"Robby Snelling","pos":"LHP","score":89,"call_up":"High","bowman":"$25-80","topps":"$80-230"},
           {"player":"Samuel Zavala","pos":"OF","score":88,"call_up":"High","bowman":"$20-65","topps":"$65-200"}],
    "SF": [{"player":"Bryce Eldridge","pos":"1B/RHP","score":89,"call_up":"High","bowman":"$25-80","topps":"$80-230"},
           {"player":"Marco Luciano","pos":"SS","score":85,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"},
           {"player":"Kyle Harrison","pos":"LHP","score":83,"call_up":"Medium","bowman":"$10-35","topps":"$30-90"}],
    "SEA":[{"player":"Colt Emerson","pos":"SS","score":88,"call_up":"High","bowman":"$25-80","topps":"$80-250"},
           {"player":"Cole Young","pos":"SS","score":87,"call_up":"High","bowman":"$20-65","topps":"$65-190"},
           {"player":"Harry Ford","pos":"C","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"}],
    "STL":[{"player":"Masyn Winn","pos":"SS","score":88,"call_up":"High","bowman":"$20-65","topps":"$65-200"},
           {"player":"Tink Hence","pos":"RHP","score":87,"call_up":"High","bowman":"$20-65","topps":"$65-190"},
           {"player":"Gordon Graceffo","pos":"RHP","score":84,"call_up":"Medium","bowman":"$10-35","topps":"$35-100"}],
    "TB": [{"player":"Carson Williams","pos":"SS","score":90,"call_up":"High","bowman":"$30-90","topps":"$90-270"},
           {"player":"Taj Bradley","pos":"RHP","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"},
           {"player":"Jonny DeLuca","pos":"OF","score":84,"call_up":"Medium","bowman":"$10-35","topps":"$35-100"}],
    "TEX":[{"player":"Wyatt Langford","pos":"OF","score":89,"call_up":"High","bowman":"$25-80","topps":"$80-230"},
           {"player":"Kumar Rocker","pos":"RHP","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"},
           {"player":"Brock Porter","pos":"RHP","score":84,"call_up":"Medium","bowman":"$10-35","topps":"$35-100"}],
    "TOR":[{"player":"Ricky Tiedemann","pos":"LHP","score":91,"call_up":"High","bowman":"$35-110","topps":"$110-320"},
           {"player":"Orelvis Martinez","pos":"SS","score":85,"call_up":"Medium","bowman":"$12-40","topps":"$40-120"},
           {"player":"Leo De Vries","pos":"SS","score":85,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"}],
    "WSN":[{"player":"James Wood","pos":"OF","score":96,"call_up":"High","bowman":"$80-250","topps":"$250-750"},
           {"player":"Dylan Crews","pos":"OF","score":89,"call_up":"High","bowman":"$25-80","topps":"$80-230"},
           {"player":"Brady House","pos":"SS","score":86,"call_up":"Medium","bowman":"$15-50","topps":"$50-150"}],
}

if "current_team" not in st.session_state:
    st.session_state.current_team = None
if "selected_player" not in st.session_state:
    st.session_state.selected_player = None

# ── TEAM SELECTION ──────────────────────────────────────────────────────────
if st.session_state.current_team is None:
    st.markdown("## ⚾ MLB Prospect Analyzer")
    st.markdown("*Trade Show Edition — Tap a team*")

    # Render pairs of teams as rows using HTML layout + real buttons underneath
    # We inject a unique div id wrapper per button and style each individually
    pairs = [(TEAMS[i], TEAMS[i+1] if i+1 < len(TEAMS) else None) for i in range(0, len(TEAMS), 2)]

    for left, right in pairs:
        cols = st.columns(2)
        for col, team_tuple in zip(cols, [left, right]):
            if team_tuple is None:
                continue
            code, name = team_tuple
            color = TEAM_COLORS.get(code, "#1c2a3e")
            with col:
                # Inject style + button together so the style scopes correctly
                st.markdown(f"""
                <style>
                div[data-testid="stButton"]:has(button[kind="secondary"]) button[kind="secondary"] {{
                    text-align: center !important;
                }}
                .btn-{code} + div .stButton > button,
                .btn-{code} ~ div .stButton > button {{
                    background: {color} !important;
                }}
                </style>
                <div class="btn-{code}"></div>
                """, unsafe_allow_html=True)
                if st.button(f"{code}\n{name}", key=f"team_{code}", use_container_width=True):
                    st.session_state.current_team = code
                    st.session_state.selected_player = None
                    st.rerun()

    # Override all team buttons with their colors using a JS injection
    js_colors = {code: color for code, color in TEAM_COLORS.items()}
    color_script = "<script>\n(function() {\n  const map = " + str(js_colors).replace("'", '"') + ";\n"
    color_script += """
  function styleButtons() {
    const buttons = document.querySelectorAll('button[kind="secondary"]');
    buttons.forEach(btn => {
      const text = btn.innerText.trim();
      const code = text.split('\\n')[0].trim();
      if (map[code]) {
        btn.style.setProperty('background', map[code], 'important');
        btn.style.setProperty('color', '#ffffff', 'important');
        btn.style.setProperty('border', '1px solid rgba(255,255,255,0.2)', 'important');
        btn.style.setProperty('border-radius', '10px', 'important');
        btn.style.setProperty('font-weight', '700', 'important');
        btn.style.setProperty('font-size', '15px', 'important');
        btn.style.setProperty('text-align', 'center', 'important');
        btn.style.setProperty('min-height', '60px', 'important');
        btn.style.setProperty('line-height', '1.3', 'important');
      }
    });
  }
  styleButtons();
  setTimeout(styleButtons, 300);
  setTimeout(styleButtons, 800);
  const obs = new MutationObserver(styleButtons);
  obs.observe(document.body, {childList: true, subtree: true});
})();
</script>"""
    st.markdown(color_script, unsafe_allow_html=True)

# ── TEAM PROSPECTS ──────────────────────────────────────────────────────────
else:
    team = st.session_state.current_team
    team_name = next(n for c, n in TEAMS if c == team)
    color = TEAM_COLORS.get(team, "#1c2a3e")

    if st.button("← Back to All Teams", key="back"):
        st.session_state.current_team = None
        st.session_state.selected_player = None
        st.rerun()

    st.markdown(f"""
    <div style="background:{color};border-radius:12px;padding:16px 20px;margin:8px 0 16px 0;
         border:1px solid rgba(255,255,255,0.2);">
        <div style="color:#ffffff;font-size:28px;font-weight:800;">{team}</div>
        <div style="color:rgba(255,255,255,0.85);font-size:16px;">{team_name} — Top Prospects</div>
    </div>
    """, unsafe_allow_html=True)

    prospects = PROSPECTS.get(team, [])

    for p in prospects:
        score = p["score"]
        if score >= 90:
            dot = "🟢"; badge_bg = "#0d2818"; badge_color = "#3fb950"
        elif score >= 85:
            dot = "🟡"; badge_bg = "#2d1f00"; badge_color = "#d29922"
        else:
            dot = "🔴"; badge_bg = "#2d0c0c"; badge_color = "#f85149"

        if st.button(f"{dot} {p['player']} ({p['pos']})  |  Score: {score}",
                     key=f"p_{p['player']}", use_container_width=True):
            st.session_state.selected_player = None if st.session_state.selected_player == p["player"] else p["player"]
            st.rerun()

        if st.session_state.selected_player == p["player"]:
            st.markdown(f"""
            <div style="background:#161b22;border:1px solid {color};border-radius:10px;
                 padding:16px 20px;margin:4px 0 12px 0;">
                <div style="color:#ffffff;font-size:20px;font-weight:700;margin-bottom:12px;">
                    {p['player']} <span style="color:rgba(255,255,255,0.5);font-size:14px;">· {p['pos']}</span>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;">
                    <div style="background:#0d1117;border-radius:8px;padding:10px 12px;border:1px solid #30475e;">
                        <div style="color:#8b949e;font-size:11px;margin-bottom:4px;">CALL-UP SCORE</div>
                        <div style="color:#ffffff;font-size:20px;font-weight:700;">{score}</div>
                        <div style="background:{badge_bg};color:{badge_color};font-size:11px;font-weight:600;
                             padding:3px 8px;border-radius:6px;display:inline-block;margin-top:4px;">{p['call_up']}</div>
                    </div>
                    <div style="background:#0d1117;border-radius:8px;padding:10px 12px;border:1px solid #30475e;">
                        <div style="color:#8b949e;font-size:11px;margin-bottom:4px;">POSITION</div>
                        <div style="color:#ffffff;font-size:20px;font-weight:700;">{p['pos']}</div>
                    </div>
                </div>
                <div style="background:#0d1117;border-radius:8px;padding:12px 14px;border:1px solid #30475e;">
                    <div style="color:#8b949e;font-size:11px;margin-bottom:8px;">🃏 CARD VALUES</div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                        <span style="color:#8b949e;font-size:13px;">Bowman Chrome</span>
                        <span style="color:#79c0ff;font-weight:600;font-size:13px;">{p['bowman']}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;">
                        <span style="color:#8b949e;font-size:13px;">Topps Auto</span>
                        <span style="color:#79c0ff;font-weight:600;font-size:13px;">{p['topps']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("✕ Close", key=f"close_{p['player']}"):
                st.session_state.selected_player = None
                st.rerun()

st.success(f"Updated {datetime.now().strftime('%I:%M %p')}")
