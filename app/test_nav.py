import streamlit as st

st.write("Testing app structure")
st.write("Current working directory:", __file__)
st.write("Session state:", dict(st.session_state))

if st.button("Go to Impact Page"):
    st.session_state["test_data"] = "Hello from dashboard"
    st.switch_page("pages/impact_page.py")
