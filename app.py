import streamlit as st

st.set_page_config(page_title="商品定制信息整理", layout="wide")

page1 = st.Page("pages/宠物陶瓷球.py", title="宠物陶瓷球")
page2 = st.Page("pages/字母图案贴画.py", title="字母图案贴画")

pg = st.navigation([page1, page2])
pg.run()