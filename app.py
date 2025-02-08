import streamlit as st

st.set_page_config(page_title="商品定制信息整理", layout="wide")


page1 = st.Page("tags/定制信息提取.py", title="定制信息提取")
page2 = st.Page("tags/苍穹定制信息处理.py", title="苍穹定制信息处理")
page3 = st.Page("tags/字母图案贴画.py", title="字母图案贴画")


pg = st.navigation({"功能列表": [page1, page2, page3]})
pg.run()
