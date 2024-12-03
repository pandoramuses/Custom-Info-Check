import streamlit as st

st.set_page_config(page_title="商品定制信息整理", layout="wide")

page1 = st.Page("pages/宠物陶瓷球.py", title="宠物陶瓷球")
page2 = st.Page("pages/字母图案贴画.py", title="字母图案贴画")
page3 = st.Page("pages/定制信息文本替换.py", title="定制信息文本替换")

pg = st.navigation({"功能列表": [page1, page2, page3]})
pg.run()