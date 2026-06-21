import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

CARDSIGHT_KEY = st.secrets.get("CARDSIGHT_API_KEY", "") or os.environ.get("CARDSIGHT_API_KEY", "")

def get_card_details(player_name):
    """Simple reliable card mock for now (images fixed)"""
    return [
        {"set": "2026 Bowman Chrome", "type": "Refractor", "price": "$25-$80", 
         "image": "https://picsum.photos/id/1015/320/420"},
        {"set": "2026 Topps Series 1", "type": "Auto", "price": "$80-$250", 
         "image": "https://picsum.photos/id/201/320/420"},
        {"set": "2026 Bowman", "type": "Base", "price": "$15-$45", 
         "image": "https://picsum.photos/id/237/320/420"},
    ]

# Data
data = [
    {"player_name": "Jesús Made", "position": "SS", "team": "MIL", "current_stats": 2.8, "base_stats": 2.3, "risk_score": 30},
    {"player_name": "Colt Emerson", "position": "SS", "team": "SEA", "current_stats": 2.7, "base_stats": 2.2, "risk_score": 32},
    {"player_name": "Leo De Vries", "position": "SS", "team": "OAK", "current_stats": 2.6, "base_stats": 2.1, "risk_score": 35},
    {"player_name": "Eli Willits", "position": "SS", "team": "WSN", "current_stats": 2.5, "base_stats": 2.0, "risk_score": 42},
    {"player_name": "Max Clark", "position": "OF", "team": "DET", "current_stats": 2.4, "base_stats": 2.0, "risk_score": 38},
    {"player_name": "Franklin Arias", "position": "SS", "team": "BOS", "current_stats": 2.5, "base_stats": 2.1, "risk_score": 36},
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
st.caption("Trade Show Edition • Tap name for card details")

with st.sidebar:
    if st.button("🔄 Refresh Card Data", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.success("✅ Refreshed!")

    search = st.text_input("🔍 Search Player")

filtered = df.copy()
if search:
    filtered = filtered[filtered["player_name"].str.contains(search, case=False)]

st.subheader(f"Prospects ({len(filtered)} shown)")
for _, row in filtered.iterrows():
    col1, col2, col3 = st.columns([5, 2, 2])
    with col1:
        if st.button(f"**{row['player_name']}** ({row['team']})", key=row['player_name']):
            st.session_state.selected_player = row['player_name']
    with col2:
        st.metric("Call-up Score", row['call_up_score'])
    with col3:
        st.write(row['recommendation'])

# Card Details
if st.session_state.get("selected_player"):
    player = st.session_state.selected_player
    row = df[df['player_name'] == player].iloc[0]
    
    st.divider()
    st.header(f"📇 {player} — Card Portfolio")
    st.write(f"{row['position']} • {row['team']} | **{row['call_up_score']}** Score")
    
    cards = get_card_details(player)
    for card in cards:
        st.image(card["image"], width=320)
        st.subheader(card["set"])
        st.write(f"**{card['type']}**")
        st.success(f"Market: {card['price']}")
        st.divider()

    if st.button("← Back to List"):
        st.session_state.selected_player = None
        st.rerun()

st.success(f"Last updated: {datetime.now().strftime('%b %d, %I:%M %p')}")
