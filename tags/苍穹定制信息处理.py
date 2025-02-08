import streamlit as st

from components.json_read_write import get_match_dict
from components.rule_check_add import rule_add
from components.file_up_down_loader import excel_file_uploader, excel_downloader
from components.custom_info_replace import title_replace, get_custom_info


# 页面布局
st.title("苍穹定制信息处理")

# 获取文件并展示数据预览
file, data = excel_file_uploader()

# 读取替换规则并输出
key_match_dict = get_match_dict("data/苍穹定制信息处理/标题替换规则.json")
key_words_list = set(key_match_dict.values())

# 打印关键词信息，便于查验是否需要补充，如果需要补充，手动输入进行补充
key_tab, add_new_tab = st.tabs(["标题替换规则", "新增替换规则"])
with key_tab:
    st.subheader("标题替换规则")
    st.json(key_match_dict, expanded=False)
with add_new_tab:
    st.subheader("新增替换规则")

    # 替换文本记录
    input_key, input_value = st.columns(2, vertical_alignment="center")
    with input_key:
        filled_key = st.text_input("输入需要替换的英文文本").strip()
    with input_value:
        filled_value = st.text_input("输入对应的中文表述").strip()

    rule_add(filled_key, filled_value, key_match_dict, "data/苍穹定制信息处理/标题替换规则.json")


# 处理完的结果提供下载链接
st.divider()
if file is not None:
    selected_keywords = st.multiselect("请选择需要提取的定制标题", key_words_list)
    data["定制属性"] = data["定制属性"].apply(lambda x: title_replace(x, key_match_dict))
    for title in selected_keywords:
        data[title] = data["定制属性"].apply(lambda x: get_custom_info(x, title))
    excel_downloader(data, "定制信息提取完成的表格")