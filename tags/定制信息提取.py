import sqlite3

import pandas as pd
import streamlit as st

from components.file_up_down_loader import excel_file_uploader, excel_downloader
from components.replace_get_custom_info import replace_custom_info, get_custom_info, format_rule_text


# 页面布局
st.title("定制信息提取")

# 获取文件并展示数据预览
file, data = excel_file_uploader()
if file is not None:
    if "定制属性" in data.columns:
        data["定制属性"] = data["定制属性"].fillna("无定制信息")


# 读取替换规则信息
conn = sqlite3.connect("./data/my_rule.db")
cur = conn.cursor()
cur.execute("select type, english, chinese from rules order by type")
rules = cur.fetchall()
rules = pd.DataFrame(rules)
rules.columns = ["类型", "英文表述", "中文表述"]


# 打印关键词信息，便于查验是否需要补充，如果需要补充，手动输入进行补充
search_tab, add_tab = st.tabs(["规则查询", "新增规则"])
with search_tab:
    type_select, rules_show = st.columns([1, 4], vertical_alignment="center")
    with type_select:
        rule_type = st.selectbox("选择要查询的分类", rules["类型"].unique())
    with rules_show:
        st.dataframe(rules[rules["类型"] == rule_type], use_container_width=True, hide_index=True)
with add_tab:
    english_key, chinese_value = st.columns(2, vertical_alignment="center")
    with english_key:
        filled_key = st.text_input("英文表述")
        format_filled_key = format_rule_text(filled_key)
    with chinese_value:
        filled_value = st.text_input("中文表述")

    type_name = filled_value.split("：")[0]

    # 规则写入数据库
    add_button = st.button(label="确认添加")
    if add_button:
        if format_filled_key not in rules["英文表述"].unique():
            try:
                cur.execute(f"""insert into rules ("type", "english", "chinese") values (?, ?, ?);""",
                            (type_name, format_filled_key, filled_value))
            except Exception as e:
                st.error(e)
            else:
                conn.commit()
                st.success("添加成功")
        else:
            st.error("对应定制信息已存在对应规则")



# 先行确认需要提取的字段
st.divider()
selected_types = st.multiselect("选择要提取的定制属性", rules["类型"].unique())

# 根据规则信息生成规则字典
rules_dict = rules[rules["类型"].isin(selected_types)].set_index("英文表述")["中文表述"].to_dict()

# 处理完的结果提供下载链接
if file is not None:
    data["替换后定制属性"] = data["定制属性"].apply(lambda x: replace_custom_info(x, rules_dict))
    # 按类型提取对应定制信息
    for title in selected_types:
        data[title] = data["替换后定制属性"].apply(lambda x: get_custom_info(x, title))
    excel_downloader(data, "定制信息提取结果")
