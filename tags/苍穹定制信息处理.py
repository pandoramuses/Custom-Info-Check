import streamlit as st

from components.json_read_write import get_match_dict
from components.rule_check_add import rule_add
from components.file_up_down_loader import excel_file_uploader, excel_downloader
from components.custom_info_replace import title_replace, get_custom_info


# 页面布局
st.title("苍穹定制信息处理")

# 获取文件并展示数据预览
file, data = excel_file_uploader()
if file is not None:
    if "定制属性" in data.columns:
        data["定制属性"] = data["定制属性"].fillna("无定制信息")

# 读取替换规则并输出
key_match_dict = get_match_dict("data/苍穹定制信息处理/标题替换规则.json")

# 打印关键词信息，便于查验是否需要补充，如果需要补充，手动输入进行补充
current_goods_type, key_tab, add_new_tab = st.tabs(["已有品类名称", "标题替换规则", "新增替换规则"])
with current_goods_type:
    st.subheader("已有品类名称")
    for key in key_match_dict.keys():
        st.write(key)
with key_tab:
    st.subheader("标题替换规则")
    st.json(key_match_dict, expanded=False)
with add_new_tab:
    st.subheader("新增替换规则")

    # 替换文本记录
    goods_type, input_key, input_value = st.columns(3, vertical_alignment="center")
    with goods_type:
        filled_goods_type = st.text_input("输入商品品类（尽量复用已有品类名称）").split("-")[0].strip()
    with input_key:
        filled_key = st.text_input("输入需要替换的英文文本").strip().lower()
    with input_value:
        filled_value = st.text_input("输入对应的中文表述").strip()

    rule_add(filled_goods_type, filled_key, filled_value, key_match_dict, "data/苍穹定制信息处理/标题替换规则.json")


# 处理完的结果提供下载链接
st.divider()
if file is not None:
    selected_goods_type = st.selectbox("请选择需要提取定制信息的品类", key_match_dict.keys())
    selected_keywords = st.multiselect("请选择需要提取的定制标题", set(key_match_dict[selected_goods_type].values()))
    data["定制属性"] = data["定制属性"].apply(lambda x: title_replace(x, key_match_dict[selected_goods_type]))
    for title in selected_keywords:
        data[title] = data["定制属性"].apply(lambda x: get_custom_info(x, title))
    excel_downloader(data, "定制信息提取完成的表格")