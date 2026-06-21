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
    
    for i, row in spreadsheet_df.iterrows():
        cols = st.columns([1, 3, 1, 1, 1, 2, 2])
        with cols[0]:
            st.write(row['rank'])
        with cols[1]:
            st.write(row['player_name'])
        with cols[2]:
            st.write(row['position'])
        with cols[3]:
            st.write(row['team'])
        with cols[4]:
            st.metric("Score", row['call_up_score'])
        with cols[5]:
            st.write(row['recommendation'])
        with cols[6]:
            if st.button("View", key=f"spread_{i}"):
                st.session_state.selected_player = row['player_name']
                st.rerun()

# Detail Page (unchanged)
else:
    player = st.session_state.selected_player
    row = df[df['player_name'] == player].iloc[0]
    
    if st.button("← Back to Main List", type="secondary"):
        st.session_state.selected_player = None
        st.rerun()
    
    st.title(f"📇 {player}")
    st.write(f"**{row['position']} • {row['team']}** | Rank: **{row['rank']}** | Call-up Score: **{row['call_up_score']}**")
    
    st.divider()
    st.header("Most Popular Cards")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://picsum.photos/id/1015/300/420", width=280)
        st.write("**2026 Bowman Chrome Refractor**")
        st.success("Price Range: $25 – $80")
    with col2:
        st.image("https://picsum.photos/id/201/300/420", width=280)
        st.write("**2026 Topps Series 1 Auto**")
        st.success("Price Range: $80 – $250")
    with col3:
        st.image("https://picsum.photos/id/237/300/420", width=280)
        st.write("**2026 Bowman Base**")
        st.success("Price Range: $15 – $45")
    
    st.divider()
    st.header("All Current Card Variations")
    card_data = pd.DataFrame({
        "Set": ["2026 Bowman Chrome", "2026 Topps Series 1", "2026 Bowman", "2026 Bowman Chrome"],
        "Variation": ["Refractor", "Auto", "Base", "Base"],
        "Price Range": ["$25-$80", "$80-$250", "$15-$45", "$20-$60"],
        "Trend": ["Rising", "Stable", "Stable", "Rising"]
    })
    st.dataframe(card_data, use_container_width=True, hide_index=True)
    
    st.divider()
    st.header("Upcoming Card Sets")
    st.write("**2026 Bowman Chrome** – Release: July 2026")
    st.link_button("Buy on Amazon (Affiliate)", "https://www.amazon.com")
    
    st.write("**2026 Topps Update Series** – Release: August 2026")
    st.link_button("Buy on eBay (Affiliate)", "https://www.ebay.com")
    
    st.write("**2026 Bowman 1st Edition** – Release: September 2026")
    st.link_button("Pre-order on Fanatics", "https://www.fanatics.com")

st.success(f"Last updated: {datetime.now().strftime('%b %d, %I:%M %p')}")
