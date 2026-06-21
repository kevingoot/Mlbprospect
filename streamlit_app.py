import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="MLB Prospect Analyzer", page_icon="⚾", layout="wide")

# Data
data = [
    {"player_name": "Jesús Made", "position": "SS", "team": "MIL", "rank": 1, "current_stats": 2.8, "base_stats": 2.3, "risk_score": 30},
    {"player_name": "Colt Emerson", "position": "SS", "team": "SEA", "rank": 2, "current_stats": 2.7, "base_stats": 2.2, "risk_score": 32},
    {"player_name": "Leo De Vries", "position": "SS", "team": "OAK", "rank": 3, "current_stats": 2.6, "base_stats": 2.1, "risk_score": 35},
    {"player_name": "Eli Willits", "position": "SS", "team": "WSN", "rank": 4, "current_stats": 2.5, "base_stats": 2.0, "risk_score": 42},
    {"player_name": "Max Clark", "position": "OF", "team": "DET", "rank": 5, "current_stats": 2.4, "base_stats": 2.0, "risk_score": 38},
    {"player_name": "Franklin Arias", "position": "SS", "team": "BOS", "rank": 6, "current_stats": 2.5, "base_stats": 2.1, "risk_score": 36},
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

# Main List View
if "selected_player" not in st.session_state or st.session_state.selected_player is None:
    st.title("⚾ MLB Prospect Analyzer")
    st.caption("Trade Show Edition • Tap 'View' for details")

    with st.sidebar:
        if st.button("🔄 Weekly Refresh", type="primary", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ Refreshed!")

        search = st.text_input("🔍 Search Player")

    filtered = df.copy()
    if search:
        filtered = filtered[filtered["player_name"].str.contains(search, case=False)]

    st.subheader(f"Prospects ({len(filtered)} shown)")
    for _, row in filtered.iterrows():
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        with col1:
            st.write(f"**{row['player_name']}** ({row['team']})")
        with col2:
            st.metric("Score", row['call_up_score'])
        with col3:
            st.write(row['recommendation'])
        with col4:
            if st.button("View", key=row['player_name']):
                st.session_state.selected_player = row['player_name']

    st.divider()
    st.subheader("Full Prospect Spreadsheet")
    spreadsheet_df = df.sort_values("rank").copy()
    spreadsheet_df["View"] = "👁️ View"
    
    # Display spreadsheet with clickable View column
    for i, row in spreadsheet_df.iterrows():
        col1, col2, col3, col4, col5, col
