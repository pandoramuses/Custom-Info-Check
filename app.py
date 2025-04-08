import streamlit as st

st.set_page_config(page_title="商品定制信息整理", layout="wide")


page1 = st.Page("tags/定制信息提取.py", title="定制信息提取")


pg = st.navigation({"功能列表": [page1]})
pg.run()
