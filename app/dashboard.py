import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from db.graph_queries import get_servers, get_impact
import ai.genai_message as genai_message

st.set_page_config(layout="wide")
st.title("🚨 Business Impact Dashboard")

# ---------- LOAD SERVERS FROM NEO4J ----------
servers = get_servers()

# ---------- SESSION STATE ----------
if "fault_server" not in st.session_state:
    st.session_state.fault_server = None

if "show_details" not in st.session_state:
    st.session_state.show_details = None

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("⚙️ Fault Control")

    selected = st.selectbox("Select server to create fault", servers)

    if st.button("Trigger Fault"):
        st.session_state.fault_server = selected

        try:
            impact_rows = get_impact(selected)

            impacts = [
                {
                    "application": row["application"],
                    "process": row["process"],
                    "service": row["service"],
                }
                for row in impact_rows
            ]

            ai_message = genai_message.generate_message(selected, impacts)

            st.success(f"Fault created on {selected}")
            st.info(f"Alert: {ai_message}")
            st.success("✅ Incident message sent to Operations Department")

        except Exception as e:
            st.success(f"Fault created on {selected}")
            st.warning(f"Could not generate alert: {str(e)}")

    if st.button("Reset System"):
        st.session_state.fault_server = None
        st.session_state.show_details = None
        st.info("System reset. All alerts cleared.")

# ---------- SERVER DASHBOARD ----------
st.subheader("🖥️ Business Server Panel")

servers_list = list(servers)

# Show 3 servers per row
for idx in range(0, len(servers_list), 3):

    server_row = servers_list[idx:idx + 3]
    cols = st.columns(3)

    for col, server in zip(cols, server_row):

        is_fault = server == st.session_state.fault_server

        if is_fault:
            bg_color = "#fdecea"
            border_color = "#f44336"
            text_color = "#b71c1c"
        else:
            bg_color = "#edf7ed"
            border_color = "#2f9936"
            text_color = "#2f9936"

        card = f"""
        <div style="
            width:100%;
            margin:15px 0;
            background-color:{bg_color};
            border:2px solid {border_color};
            border-radius:12px;
            height:70px;
            display:flex;
            align-items:center;
            justify-content:center;
            color:{text_color};
            font-weight:bold;
            box-shadow:0 2px 6px rgba(0,0,0,0.1);
            font-size:16px;
            text-align:center;">
            {server}
        </div>
        """

        with col:
            st.markdown(card, unsafe_allow_html=True)

            if is_fault:
                if st.button("Show Impact Details", key=f"expand_{server}"):
                    st.session_state.show_details = server

# ---------- IMPACT DETAILS ----------
if st.session_state.show_details:

    selected_server = st.session_state.show_details

    # 🔥 ALWAYS fetch impact first
    impact_rows = get_impact(selected_server)

    # Safety check
    if not impact_rows:
        st.warning("No impact data found.")
        st.stop()

    st.divider()
    st.markdown(f"### ⚠️ Impact Details — {selected_server}")

    # Show 3 cards per row
    for idx in range(0, len(impact_rows), 3):

        row_cards = impact_rows[idx:idx + 3]
        cols_impact = st.columns(3)

        for col, item in zip(cols_impact, row_cards):

            impact_card = f"""
            <div style="
                background:#fff3cd;
                border-left:6px solid #ff9800;
                padding:12px;
                margin:8px 0;
                border-radius:8px;
                box-shadow:0 2px 4px rgba(0,0,0,0.08);
                min-height:110px;
            ">
                <b>📦 Application:</b> {item['application']}<br>
                <b>⚙️ Process:</b> {item['process']}<br>
                <b>🔗 Service:</b> {item['service']}
            </div>
            """

            with col:
                st.markdown(impact_card, unsafe_allow_html=True)

    if st.button("➡️ Open Full Impact Page"):

        st.session_state["impact_data"] = impact_rows
        st.session_state["impact_server"] = selected_server
        st.switch_page("pages/impact_page.py")
