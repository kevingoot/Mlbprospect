import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

# Fresh Data
data = [
    {"player_name": "Jesús Made", "team": "MIL", "rank": 1, "call_up_score": 92, "recommendation": "🚀 Strong Buy"},
    {"player_name": "Colt Emerson", "team": "SEA", "rank": 2, "call_up_score": 88, "recommendation": "🚀 Strong Buy"},
    {"player_name": "Leo De Vries", "team": "OAK", "rank": 3, "call_up_score": 85, "recommendation": "📈 Buy/Hold"},
    {"player_name": "Eli Willits", "team": "WSN", "rank": 4, "call_up_score": 78, "recommendation": "📈 Buy/Hold"},
    {"player_name": "Max Clark", "team": "DET", "rank": 5, "call_up_score": 82, "recommendation": "🚀 Strong Buy"},
    {"player_name": "Franklin Arias", "team": "BOS", "rank": 6, "call_up_score": 79, "recommendation": "📈 Buy/Hold"},
]

df = pd.DataFrame(data)

st.title("MLB Prospect Dashboard")
st.caption("Trade Show Ready • Click View for full breakdown")

with st.sidebar:
    if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.success("✅ Data refreshed!")

    search = st.text_input("Search Prospects")

filtered = df.copy()
if search:
    filtered = filtered[filtered["player_name"].str.contains(search, case=False)]

# Main Prospects
st.subheader("Key Prospects")
for _, row in filtered.iterrows():
    col1, col2, col3 = st.columns([4, 2, 2])
    with col1:
        st.write(f"**{row['player_name']}** ({row['team']})")
    with col2:
        st.metric("Call-up Score", row['call_up_score'])
    with col3:
        if st.button("View", key=row['player_name']):
            st.session_state.selected_player = row['player_name']

st.divider()

# Spreadsheet Focus
st.subheader("Full Prospect Spreadsheet")
spreadsheet_df = filtered.sort_values("rank")

for i, row in spreadsheet_df.iterrows():
    cols = st.columns([1, 3, 1, 2, 2])
    with cols[0]:
        st.write(row['rank'])
    with cols[1]:
        st.write(row['player_name'])
    with cols[2]:
        st.write(row['team'])
    with cols[3]:
        st.metric("Score", row['call_up_score'])
    with cols[4]:
        if st.button("View", key=f"spread_{i}"):
            st.session_state.selected_player = row['player_name']
            st.rerun()

# Detail View
if "selected_player" in st.session_state and st.session_state.selected_player:
    player = st.session_state.selected_player
    row = df[df['player_name'] == player].iloc[0]
    
    if st.button("← Back to Spreadsheet"):
        st.session_state.selected_player = None
        st.rerun()
    
    st.title(f"{player}")
    st.write(f"Team: **{row['team']}** | Call-up Score: **{row['call_up_score']}**")
    
    st.divider()
    st.header("Popular Cards")
    st.write("**Bowman Chrome Refractor** - $25-$80")
    st.write("**Topps Auto** - $80-$250")
    
    st.divider()
    st.header("Upcoming Sets")
    st.link_button("Bowman Chrome (July)", "https://www.amazon.com")
    st.link_button("Topps Update (August)", "https://www.ebay.com")

st.success(f"Updated: {datetime.now().strftime('%b %d, %I:%M %p')}")
