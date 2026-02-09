import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import ai.genai_message as genai_message

st.set_page_config(layout="wide")
st.title("🔥 Business Impact Analysis")

# ---------- DEBUG ----------
import traceback

# ---------- SESSION CHECK ----------
if "impact_data" not in st.session_state or not st.session_state.get("impact_data"):
    st.error("❌ No fault data received from dashboard.")
    st.info("Session state keys:", st.session_state.keys())
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Back to Dashboard"):
            st.switch_page("dashboard.py")
    st.stop()

data = st.session_state["impact_data"]  # 🔥 list of impacted rows

# ---------- SUMMARY HEADER ----------
server_name = data[0]["server"]  # all rows share same server

st.error(f"⚠️ Fault detected on **{server_name}**")

st.markdown("### Impact Summary")

# ---------- LIST ALL IMPACTS ----------
for i, item in enumerate(data, 1):
    st.write(f"""
**Impact {i}:**

- **Application:** {item['application']}
- **Business Process:** {item['process']}
- **Service Affected:** {item['service']}
""")

st.markdown("---")

# ---------- BUSINESS CONSEQUENCES ----------
services = ", ".join({item["service"] for item in data})

st.markdown("### Business Consequences")

st.warning(f"""
🚨 Service disruption affecting:

**{services}**

This may cause:

- Payment or transaction delays
- Customer dissatisfaction
- Revenue impact
- Operational slowdown
""")

st.markdown("---")

# ---------- AI INCIDENT MESSAGE ----------
st.markdown("### AI-Generated Incident Alert")

try:
    impacts = [
        {
            "application": item["application"],
            "service": item["service"],
        }
        for item in data
    ]

    ai_message = genai_message.generate_message(server_name, impacts)

    st.info(f"**Message:** {ai_message}")
    st.success("✅ Alert message sent to **Incident Management Department**")

except Exception as e:
    st.error(f"Failed to generate alert: {str(e)}")

# ---------- NAVIGATION ----------
st.markdown("---")
if st.button("🔙 Back to Dashboard", use_container_width=True):
    st.switch_page("dashboard.py")
