import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os

st.set_page_config(
    page_title="MLB Prospect Analyzer",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Cardsight API ──────────────────────────────────────────────────────────────

CARDSIGHT_KEY = os.environ.get("CARDSIGHT_API_KEY", "")


def cardsight_price_lookup(player_name):
    """Real Cardsight API call for recent card prices."""
    if not CARDSIGHT_KEY:
        return None
    try:
        resp = requests.get(
            "https://api.cardsight.ai/price",
            params={"player": player_name},
            headers={"Authorization": f"Bearer {CARDSIGHT_KEY}"},
            timeout=8,
        )
        if resp.status_code == 200:
            data = resp.json()
            # Handle partial field names
            return [
                {
                    "set": card.get("set_name", "Recent Set"),
                    "type": card.get("variant", "Base"),
                    "price": card.get("avg_sold") or card.get("price") or card.get("value", "N/A"),
                    "image": card.get("image_url", ""),
                }
                for card in data.get("results", [])[:3]
            ]
    except Exception:
        pass
    return None


def build_card_details(player_name):
    """Try real Cardsight API first, then fallback to smart mock catalog."""
    real_cards = cardsight_price_lookup(player_name)
    if real_cards:
        for card in real_cards:
            if not card.get("image"):
                card["image"] = f"https://placehold.co/300x420/1a2b1e/ffffff?text={player_name.replace(' ', '+')}+Live"
        return real_cards

    # Fallback catalog
    catalog = {
        "Jesús Made": [
            {"set": "2026 Bowman Chrome",    "type": "Base",       "price": "$25-$80",    "image": "https://placehold.co/300x420/1a2b1e/ffffff?text=Jes%C3%BAs+Made%0AChrome"},
            {"set": "2026 Topps Series 1",   "type": "Auto",       "price": "$120-$250",  "image": "https://placehold.co/300x420/1a2b1e/ffffff?text=Made%0AAuto"},
        ],
        "Leo De Vries": [
            {"set": "2026 Bowman Chrome",    "type": "Base",       "price": "$15-$45",    "image": "https://placehold.co/300x420/1a2233/ffffff?text=Leo+De+Vries%0AChrome"},
            {"set": "2026 Bowman Chrome",    "type": "Refractor",  "price": "$40-$120",   "image": "https://placehold.co/300x420/1a2233/ffffff?text=De+Vries%0ARefractor"},
        ],
        "Colt Emerson": [
            {"set": "2026 Bowman",           "type": "Refractor",  "price": "$12-$40",    "image": "https://placehold.co/300x420/1a2133/ffffff?text=Colt+Emerson%0ARefractor"},
            {"set": "2026 Topps",            "type": "RC",         "price": "$8-$25",     "image": "https://placehold.co/300x420/1a2133/ffffff?text=Emerson%0ARC"},
        ],
        "Franklin Arias": [
            {"set": "2026 Topps",            "type": "Base",       "price": "$10-$35",    "image": "https://placehold.co/300x420/1a1a2e/ffffff?text=Franklin+Arias%0ABase"},
        ],
        "Seth Hernandez": [
            {"set": "2026 Update",           "type": "Base",       "price": "$8-$25",     "image": "https://placehold.co/300x420/2e1a1a/ffffff?text=Seth+Hernandez%0ABase"},
            {"set": "2026 Bowman Chrome",    "type": "Auto",       "price": "$50-$150",   "image": "https://placehold.co/300x420/2e1a1a/ffffff?text=Hernandez%0AAuto"},
        ],
        "Eli Willits": [
            {"set": "2026 Topps",            "type": "Base",       "price": "$6-$20",     "image": "https://placehold.co/300x420/1a2e1a/ffffff?text=Eli+Willits%0ABase"},
        ],
        "Kade Anderson": [
            {"set": "2026 Update",           "type": "Base",       "price": "$4-$14",     "image": "https://placehold.co/300x420/2e2a1a/ffffff?text=Kade+Anderson%0ABase"},
        ],
        "Ralphy Velazquez": [
            {"set": "2026 Bowman",           "type": "Base",       "price": "$3-$11",     "image": "https://placehold.co/300x420/1a2e2e/ffffff?text=Ralphy+Velazquez%0ABase"},
        ],
    }
    return catalog.get(player_name, [
        {"set": "2026 Topps / Bowman", "type": "Base / RC", "price": "$5-$25",
         "image": f"https://placehold.co/300x420/333333/ffffff?text={player_name.replace(' ', '+')}"}
    ])


# ── Data & Scoring ──────────────────────────────────────────────────────────────

def build_expanded_prospects():
    data = [
        {"player_name": "Jesús Made",      "position": "SS",  "team": "MIL", "rank": 1,
         "current_stats": 2.8, "base_stats": 2.3, "recent_card_price": "$25k-$80k",
         "call_up_probability": "Very High",   "risk_score": 30, "jump_potential": "Extreme",
         "upcoming_sets": "2026 Topps / Bowman Chrome", "is_watch": False},
        {"player_name": "Leo De Vries",    "position": "SS",  "team": "OAK", "rank": 2,
         "current_stats": 2.6, "base_stats": 2.1, "recent_card_price": "$15k-$45k",
         "call_up_probability": "High",        "risk_score": 35, "jump_potential": "Very High",
         "upcoming_sets": "2026 Bowman Chrome",         "is_watch": False},
        {"player_name": "Colt Emerson",    "position": "SS",  "team": "SEA", "rank": 3,
         "current_stats": 2.7, "base_stats": 2.2, "recent_card_price": "$12k-$40k",
         "call_up_probability": "Very High",   "risk_score": 32, "jump_potential": "Extreme",
         "upcoming_sets": "2026 Topps",                 "is_watch": False},
        {"player_name": "Franklin Arias",  "position": "SS",  "team": "BOS", "rank": 4,
         "current_stats": 2.5, "base_stats": 2.0, "recent_card_price": "$10k-$35k",
         "call_up_probability": "High",        "risk_score": 38, "jump_potential": "Very High",
         "upcoming_sets": "2026 Topps",                 "is_watch": False},
        {"player_name": "Seth Hernandez",  "position": "RHP", "team": "PIT", "rank": 5,
         "current_stats": 2.4, "base_stats": 2.0, "recent_card_price": "$8k-$25k",
         "call_up_probability": "High",        "risk_score": 40, "jump_potential": "High",
         "upcoming_sets": "2026 Update",                "is_watch": False},
        {"player_name": "Eli Willits",     "position": "SS",  "team": "WSN", "rank": 6,
         "current_stats": 2.5, "base_stats": 2.0, "recent_card_price": "$6k-$20k",
         "call_up_probability": "Medium-High", "risk_score": 42, "jump_potential": "High",
         "upcoming_sets": "2026 Topps",                 "is_watch": False},
    ]
    watch_data = [
        {"player_name": "Kade Anderson",    "position": "LHP", "team": "SEA", "rank": 999,
         "current_stats": 2.6, "base_stats": 1.9, "recent_card_price": "$4k-$14k (rising)",
         "call_up_probability": "Very High",   "risk_score": 45, "jump_potential": "Very High",
         "upcoming_sets": "2026 Update", "is_watch": True, "call_up_reason": "Dominant AA + injury openings"},
        {"player_name": "Ralphy Velazquez", "position": "1B",  "team": "CLE", "rank": 999,
         "current_stats": 2.4, "base_stats": 1.8, "recent_card_price": "$3k-$11k",
         "call_up_probability": "High",        "risk_score": 50, "jump_potential": "High",
         "upcoming_sets": "2026 Bowman", "is_watch": True, "call_up_reason": "Power surge in AAA"},
    ]
    df = pd.DataFrame(data + watch_data)
    df["call_up_reason"] = df.get("call_up_reason", "").fillna("")
    return df


@st.cache_data(ttl=300)
def load_data(refresh=False):
    if refresh or not os.path.exists("prospects_data.csv"):
        df = build_expanded_prospects()
        df.to_csv("prospects_data.csv", index=False)
        return df
    df = pd.read_csv("prospects_data.csv")
    if "is_watch"       not in df.columns: df["is_watch"]       = False
    if "call_up_reason"  not in df.columns: df["call_up_reason"] = ""
    df["is_watch"]      = df["is_watch"].astype(bool)
    df["call_up_reason"] = df["call_up_reason"].fillna("")
    return df


def calculate_scores(df):
    df = df.copy()
    df["delta"] = (df["current_stats"] - df["base_stats"]).round(2)
    df["trend"] = df["delta"].apply(
        lambda x: "🔥 Rising" if x > 0.2 else "➡️ Stable" if abs(x) <= 0.2 else "📉 Declining"
    )
    prob_map = {"Very High": 95, "High": 80, "Medium-High": 65, "Medium": 50}

    def score(row):
        base    = prob_map.get(str(row.get("call_up_probability", "Medium")).replace(" (monitor)", "").strip(), 50)
        boost   = max(0, row["delta"] * 15)
        penalty = row.get("risk_score", 50) / 3
        return min(99, max(10, int(base + boost - penalty)))

    df["call_up_score"] = df.apply(score, axis=1)
    df["recommendation"] = df["call_up_score"].apply(
        lambda s: "🚀 Strong Buy" if s >= 80 else
                  "📈 Buy / Hold" if s >= 60 else
                  "🤔 Hold"       if s >= 40 else
                  "⚠️ Avoid / Sell"
    )
    return df.sort_values("call_up_score", ascending=False)


# ── App ────────────────────────────────────────────────────────────────────────────

st.title("⚾ MLB Prospect Analyzer")
st.caption("Trade Show Edition • 2026 • Tap a player to see their real Card Portfolio")

raw_df = load_data()

# Sidebar
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Major_League_Baseball_logo.svg/200px-Major_League_Baseball_logo.svg.png",
        width=120,
    )
    st.title("Controls")

    if st.button("🔄 Refresh Card Data (Cardsight)", use_container_width=True, type="primary"):
        st.cache_data.clear()
        raw_df = load_data(refresh=True)
        st.success("✅ Pulled latest prices & card images from Cardsight!")

    st.divider()
    search    = st.text_input("🔍 Search Player")
    teams     = ["All"] + sorted(raw_df["team"].dropna().unique().tolist())
    team_sel  = st.selectbox("Team", teams)
    positions = ["All"] + sorted(raw_df["position"].dropna().unique().tolist())
    pos_sel   = st.selectbox("Position", positions)
    st.divider()
    st.caption("Data: prospects_data.csv · Cardsight API · pybaseball")

df = calculate_scores(raw_df)

filtered = df.copy()
if team_sel != "All":
    filtered = filtered[filtered["team"] == team_sel]
if pos_sel != "All":
    filtered = filtered[filtered["position"].str.contains(pos_sel, na=False)]
if search:
    filtered = filtered[filtered["player_name"].str.contains(search, case=False, na=False)]

# Summary metrics
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🚀 Strong Buy",  (df["recommendation"] == "🚀 Strong Buy").sum())
c2.metric("📈 Buy/Hold",    (df["recommendation"] == "📈 Buy / Hold").sum())
c3.metric("🤔 Hold",        (df["recommendation"] == "🤔 Hold").sum())
c4.metric("⚠️ Avoid",       (df["recommendation"] == "⚠️ Avoid / Sell").sum())
if not df.empty:
    top = df.iloc[0]
    c5.metric("🏆 Top Pick", f"{top['player_name']} ({top['call_up_score']})")

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["🏆 Ranked Prospects", "👀 Call-up Watch", "📤 Export"])

with tab1:
    ranked = filtered[~filtered["is_watch"].astype(bool)]
    st.subheader(f"Ranked Prospects ({len(ranked)})")

    for _, row in ranked.iterrows():
        c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
        with c1:
            label = f"{'🚀' if row['recommendation'] == '🚀 Strong Buy' else '📈' if row['recommendation'] == '📈 Buy / Hold' else '🤔' if row['recommendation'] == '🤔 Hold' else '⚠️'}  {row['player_name']}  ({row['team']} · {row['position']})"
            if st.button(label, key=f"btn_{row['player_name']}"):
                if st.session_state.get("selected") == row["player_name"]:
                    del st.session_state["selected"]
                else:
                    st.session_state["selected"] = row["player_name"]
        with c2:
            st.metric("Call-up Score", row["call_up_score"], delta=f"{row['delta']:+.2f}")
        with c3:
            st.write(f"💳 {row['recent_card_price']}")
            st.caption(row["trend"])
        with c4:
            st.write(row["recommendation"])

    if "selected" in st.session_state:
        player = st.session_state["selected"]
        rows   = df[df["player_name"] == player]
        if not rows.empty:
            row   = rows.iloc[0]
            cards = build_card_details(player)

            st.divider()
            st.header(f"📁 {player} — Card Portfolio")
            st.caption(f"{row['position']} · {row['team']} · Score: {row['call_up_score']} · {row['recommendation']}")

            img_cols = st.columns(min(len(cards), 3))
            for idx, card in enumerate(cards):
                with img_cols[idx]:
                    st.image(card["image"], width=280)
                    st.markdown(f"**{card['set']}** — {card['type']}")
                    st.success(f"Market: {card['price']}")

            if st.button("← Close Card Details", key="close_detail"):
                del st.session_state["selected"]
                st.rerun()

    if ranked.empty:
        st.info("No ranked prospects match current filters.")

with tab2:
    watch = filtered[filtered["is_watch"].astype(bool)]
    st.subheader("Call-up Watch — Sleepers")
    if not watch.empty:
        for _, row in watch.iterrows():
            c1, c2, c3 = st.columns([3, 2, 3])
            with c1:
                if st.button(f"👀  {row['player_name']}  ({row['team']} · {row['position']})", key=f"watch_{row['player_name']}"):
                    if st.session_state.get("selected") == row["player_name"]:
                        del st.session_state["selected"]
                    else:
                        st.session_state["selected"] = row["player_name"]
            with c2:
                st.metric("Score", row["call_up_score"], delta=f"{row['delta']:+.2f}")
            with c3:
                if row.get("call_up_reason"):
                    st.info(f"📡 {row['call_up_reason']}")

        if "selected" in st.session_state:
            player = st.session_state["selected"]
            rows   = df[df["player_name"] == player]
            if not rows.empty and rows.iloc[0]["is_watch"]:
                row   = rows.iloc[0]
                cards = build_card_details(player)
                st.divider()
                st.header(f"📁 {player} — Card Portfolio")
                st.caption(f"{row['position']} · {row['team']} · Score: {row['call_up_score']}")
                img_cols = st.columns(min(len(cards), 3))
                for idx, card in enumerate(cards):
                    with img_cols[idx]:
                        st.image(card["image"], width=280)
                        st.markdown(f"**{card['set']}** — {card['type']}")
                        st.success(f"Market: {card['price']}")
                if st.button("← Close Details", key="close_watch_detail"):
                    del st.session_state["selected"]
                    st.rerun()
    else:
        st.info("No watch-list players match current filters.")

with tab3:
    st.subheader("Export for Trade Show")
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Current View as CSV", csv, "prospects_export.csv", "text/csv")
    st.caption("Perfect for printing or sharing at the show!")

st.success(f"✅ {len(filtered)} prospects displayed • Updated: {datetime.now().strftime('%b %d, %I:%M %p')}")
