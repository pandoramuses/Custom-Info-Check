import streamlit as st

st.set_page_config(page_title="商品定制信息整理", layout="wide")


page1 = st.Page("tags/宠物陶瓷球.py", title="宠物陶瓷球")
page2 = st.Page("tags/字母图案贴画.py", title="字母图案贴画")
page3 = st.Page("tags/定制信息文本替换.py", title="定制信息文本替换")
page4 = st.Page("tags/服装规格信息提取.py", title="服装规格信息提取")
page5 = st.Page("tags/玩具汽车车型提取.py", title="玩具汽车车型提取")

pg = st.navigation({"功能列表": [page1, page2, page3, page4, page5]})
pg.run()
