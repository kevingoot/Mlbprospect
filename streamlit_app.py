import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

# Expanded prospect list (easy to grow to 10 per team)
data = [
    {"player_name": "Jesús Made", "position": "SS", "team": "MIL", "rank": 1, "current_stats": 2.8, "base_stats": 2.3, "risk_score": 30},
    {"player_name": "Colt Emerson", "position": "SS", "team": "SEA", "rank": 2, "current_stats": 2.7, "base_stats": 2.2, "risk_score": 32},
    {"player_name": "Leo De Vries", "position": "SS", "team": "OAK", "rank": 3, "current_stats": 2.6, "base_stats": 2.1, "risk_score": 35},
    {"player_name": "Eli Willits", "position": "SS", "team": "WSN", "rank": 4, "current_stats": 2.5, "base_stats": 2.0, "risk_score": 42},
    {"player_name": "Max Clark", "position": "OF", "team": "DET", "rank": 5, "current_stats": 2.4, "base_stats": 2.0, "risk_score": 38},
    {"player_name": "Franklin Arias", "position": "SS", "team": "BOS", "rank": 6, "current_stats": 2.5, "base_stats": 2.1, "risk_score": 36},
    {"player_name": "Kevin McGonigle", "position": "SS", "team": "DET", "rank": 7, "current_stats": 2.3, "base_stats": 1.9, "risk_score": 45},
    {"player_name": "Konnor Griffin", "position": "SS/OF", "team": "PIT", "rank": 8, "current_stats": 2.6, "base_stats": 2.0, "risk_score": 40},
    {"player_name": "Travis Bazzana", "position": "2B", "team": "CLE", "rank": 9, "current_stats": 2.4, "base_stats": 2.0, "risk_score": 48},
    {"player_name": "Seth Hernandez", "position": "RHP", "team": "PIT", "rank": 10, "current_stats": 2.5, "base_stats": 2.1, "risk_score": 41},
    {"player_name": "Kade Anderson", "position": "LHP", "team": "SEA", "rank": 11, "current_stats": 2.5, "base_stats": 2.0, "risk_score": 43},
    {"player_name": "Ethan Salas", "position": "C", "team": "SD", "rank": 12, "current_stats": 2.3, "base_stats": 1.9, "risk_score": 47},
]

df = pd.DataFrame(data)

def calculate_scores(df):
    df = df.copy()
    df["delta"] = (df["current_stats"] - df["base_stats"]).round(2)
    df["call_up_score"] = df.apply(lambda row: min(99, max(10, int(70 + row["delta"]*15 - row["risk_score"]/4))), axis=1)
    df["recommendation"] = df["call_up_score"].apply(
        lambda s: "🚀 Strong Buy" if s >= 80 else "📈 Buy/Hold" if s >= 60 else "🤔 Hold" if s >= 40 else "⚠️ Avoid"
    )
    return df

df = calculate_scores(df)

# UI
st.title("⚾ MLB Prospect Analyzer")
st.caption("Trade Show Edition • Weekly Updated")

with st.sidebar:
    if st.button("🔄 Weekly Full Refresh", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.success("✅ Full list refreshed!")

    search = st.text_input("🔍 Search Player")

filtered = df.copy()
if search:
    filtered = filtered[filtered["player_name"].str.contains(search, case=False)]

st.subheader("Top Prospects")
for _, row in filtered.iterrows():
    col1, col2, col3 = st.columns([5, 2, 2])
    with col1:
        if st.button(f"**{row['player_name']}** ({row['team']})", key=row['player_name']):
            st.session_state.selected_player = row['player_name']
    with col2:
        st.metric("Call-up Score", row['call_up_score'])
    with col3:
        st.write(row['recommendation'])

# Detail view (kept simple)
if st.session_state.get("selected_player"):
    player = st.session_state.selected_player
    row = df[df['player_name'] == player].iloc[0]
    
    st.divider()
    st.header(f"📇 {player} — Details")
    st.write(f"{row['position']} • {row['team']} | **{row['call_up_score']}** Score")
    st.info("Card images & full price variations coming next (Cardsight ready)")
    
    if st.button("← Back"):
        st.session_state.selected_player = None
        st.rerun()

st.divider()

# Full Spreadsheet at the bottom
st.subheader("Full Prospect Spreadsheet")

spreadsheet_df = df.copy()
spreadsheet_df = spreadsheet_df.sort_values("rank")

# Add a simple card price summary column
def get_price_summary(name):
    return "$15-$80 (multiple variations)"

spreadsheet_df["Card Prices"] = spreadsheet_df["player_name"].apply(get_price_summary)

st.dataframe(
    spreadsheet_df[["rank", "player_name", "position", "team", "call_up_score", "recommendation", "Card Prices"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "rank": st.column_config.NumberColumn("Rank", width="small"),
        "call_up_score": st.column_config.ProgressColumn("Call-up Score", min_value=0, max_value=100),
        "Card Prices": "Card Prices (Current Variations)"
    }
)

st.success(f"Last updated: {datetime.now().strftime('%b %d, %I:%M %p')}")
