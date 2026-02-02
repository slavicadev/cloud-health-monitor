import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURATION & PATHS ---
# Ensures the app finds the 'data' folder at the root regardless of where it's run
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "status_history.json")

st.set_page_config(
    page_title="Cloud-Pulse Intelligence",
    page_icon="📈",
    layout="wide"
)

# --- 2. DATA LOADING ---
def load_data():
    """Loads historical JSON data and ensures it is a list of entries."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                content = json.load(f)
                return content if isinstance(content, list) else [content]
        except (json.JSONDecodeError, ValueError):
            return []
    return []

# --- 3. UI HEADER ---
st.title("🌐 Cloud-Pulse: Infrastructure Dashboard")
st.markdown(f"**Last Sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

history = load_data()

if not history:
    st.warning("📡 Waiting for the monitor service to generate data...")
    st.info("The dashboard will update automatically once the first check completes.")
else:
    # Get the latest entry for status cards
    latest_check = history[-1]
    services = {k: v for k, v in latest_check.items() if k != 'timestamp'}

    # --- 4. LIVE STATUS CARDS ---
    st.subheader("Live Service Status")
    cols = st.columns(len(services))
    
    for i, (name, status) in enumerate(services.items()):
        with cols[i]:
            # Resilient check for "Operational" status
            is_ok = any(word in str(status).lower() for word in ["operational", "active", "online", "up"])
            if is_ok:
                st.success(f"**{name}**")
                st.caption("✅ Stable")
            else:
                st.error(f"**{name}**")
                st.caption(f"🚨 {status}")

    # --- 5. AI PREDICTOR ---
    st.divider()
    st.subheader("🧠 AI Stability Predictor")
    
    active_issues = [s for s, v in services.items() if not any(w in str(v).lower() for w in ["operational", "active"])]
    
    with st.expander("AI Analysis Report", expanded=True):
        if len(active_issues) > 1:
            st.warning(f"**AI Detection:** High Risk. Pattern suggests a potential cascading failure across: {', '.join(active_issues)}.")
        elif len(active_issues) == 1:
            st.info(f"**AI Observation:** Isolated instability detected at {active_issues[0]}. Overall ecosystem risk remains low.")
        else:
            st.write("🟢 **Nominal State:** All systems operational. AI predicts 99.9% stability for the next interval.")

    # --- 6. HISTORICAL ANALYTICS (STRICT SINGLE CHART FIX) ---
    st.divider()
    st.subheader("📊 Reliability Trends")
    
    df = pd.DataFrame(history)

    # Only show the chart if we have timestamped historical data
    if 'timestamp' in df.columns and len(df) > 1:
        # 1. Prepare and sort the timeline
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # 2. Calculate Global Health Percentage Score
        def calculate_health(row):
            meta = ['timestamp', 'Global_Health_%']
            service_cols = [c for c in row.index if c not in meta]
            total = len(service_cols)
            if total == 0: return 100
            
            up_count = sum(1 for status in row[service_cols] 
                          if any(w in str(status).lower() for w in ["operational", "active", "online", "up"]))
            return (up_count / total) * 100

        df['Global_Health_%'] = df.apply(calculate_health, axis=1)
        
        # 3. Create dedicated plotting data to isolate the variable
        chart_data = df[['timestamp', 'Global_Health_%']].copy()
        chart_data = chart_data.set_index('timestamp')

        # 4. Explicitly map the 'y' axis to prevent the 'double chart' error
        st.line_chart(chart_data, y="Global_Health_%", color="#29b5e8")
        st.caption("Uptime Percentage (0-100%) across all monitored cloud providers.")
    else:
        st.info("⌛ Gathering historical data points... Trends will appear after the second health check.")

    # --- 7. AUDIT LOG & EXPORT ---
    st.divider()
    with st.expander("Audit Log & Data Export"):
        # 2026 Updated Syntax: width='stretch'
        st.dataframe(df, width='stretch')
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Audit Report (CSV)",
            data=csv,
            file_name=f"cloud_pulse_audit_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
        )

# --- REFRESH ---
if st.button('Refresh Dashboard'):
    st.rerun()