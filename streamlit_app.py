import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

# Cardsight API (add key in Streamlit Secrets)
CARDSIGHT_KEY = os.environ.get("CARDSIGHT_API_KEY", "")

def get_card_details(player_name):
    """Fetch real card data via Cardsight or use fallback"""
    if CARDSIGHT_KEY:
        try:
            resp = requests.get(
                "https://api.cardsight.ai/v1/pricing/search",
                params={"q": player_name, "sport": "baseball"},
                headers={"Authorization": f"Bearer {CARDSIGHT_KEY}"},
                timeout=10
            )
            if resp.status_code == 200:
                results = resp.json().get("results", [])[:3]
                if results:
                    return [{
                        "set": r.get("set_name", "2026 Set"),
                        "type": r.get("variant", "Base"),
                        "price": f"${r.get('avg_sold', 'N/A')}",
                        "image": r.get("image_url") or f"https://via.placeholder.com/280x400/1a2b1e/ffffff?text={player_name.replace(' ','+')}"
                    } for r in results]
        except:
            pass
    
    # Fallback
    return [
        {"set": "2026 Bowman Chrome", "type": "Refractor", "price": "$25-$80", 
         "image": f"https://via.placeholder.com/280x400/1a2b1e/ffffff?text={player_name.replace(' ','+')}"},
        {"set": "2026 Topps Series 1", "type": "Auto", "price": "$80-$250", 
         "image": f"https://via.placeholder.com/280x400/1a2133/ffffff?text={player_name.replace(' ','+')}+Auto"},
    ]

# Sample Data (expand later)
data = [
    {"player_name": "Jesús Made", "position": "SS", "team": "MIL", "current_stats": 2.8, "base_stats": 2.3,
     "recent_card_price": "$25k-$80k", "call_up_probability": "Very High", "risk_score": 30, "jump_potential": "Extreme"},
    {"player_name": "Colt Emerson", "position": "SS", "team": "SEA", "current_stats": 2.7, "base_stats": 2.2,
     "recent_card_price": "$12k-$40k", "call_up_probability": "Very High", "risk_score": 32, "jump_potential": "Extreme"},
    {"player_name": "Leo De Vries", "position": "SS", "team": "OAK", "current_stats": 2.6, "base_stats": 2.1,
     "recent_card_price": "$15k-$45k", "call_up_probability": "High", "risk_score": 35, "jump_potential": "Very High"},
    {"player_name": "Eli Willits", "position": "SS", "team": "WSN", "current_stats": 2.5, "base_stats": 2.0,
     "recent_card_price": "$6k-$20k", "call_up_probability": "High", "risk_score": 42, "jump_potential": "High"},
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
st.caption("Trade Show Edition • Click player for card details")

with st.sidebar:
    if st.button("🔄 Weekly Cardsight Refresh", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.success("Card data refreshed!")

    search = st.text_input("🔍 Search Player")

# Filter
filtered = df.copy()
if search:
    filtered = filtered[filtered["player_name"].str.contains(search, case=False)]

# Display
st.subheader("Prospects")
for _, row in filtered.iterrows():
    col1, col2, col3 = st.columns([5, 2, 2])
    with col1:
        if st.button(f"**{row['player_name']}** ({row['team']})", key=row['player_name']):
            st.session_state.selected_player = row['player_name']
    with col2:
        st.metric("Call-up Score", row['call_up_score'])
    with col3:
        st.write(row['recommendation'])

# Card Detail View
if st.session_state.get("selected_player"):
    player = st.session_state.selected_player
    row = df[df['player_name'] == player].iloc[0]
    
    st.divider()
    st.header(f"📇 {player} — Card Details")
    st.write(f"{row['position']} • {row['team']} | Score: **{row['call_up_score']}**")
    
    cards = get_card_details(player)
    cols = st.columns(2)
    for i, card in enumerate(cards):
        with cols[i % 2]:
            st.image(card["
