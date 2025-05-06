import streamlit as st

# 서브페이지 import
from pages import overview, process, process_heatmap, monetization, table, Premise

st.set_page_config(page_title="LCA Dashboard", layout="wide")

# 페이지 선택
page = st.sidebar.selectbox("📂 Select the page", [
    "Overview",
    "Process Analysis",
    "Process Heatmap",
    "Monetization",
    "Table",
    "Premise"
])

# 각 페이지 실행
if page == "Overview":
    overview.app()
elif page == "Process Analysis":
    process.app()
elif page == "Process Heatmap":
    process_heatmap.app()
elif page == "Monetization":
    monetization.app()
elif page == "Table":
    table.app()
elif page == "Premise":
    Premise.app()