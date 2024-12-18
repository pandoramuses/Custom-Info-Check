import streamlit as st

from components.json_read_write import get_match_dict
from components.rule_check_add import rule_check, rule_add
from components.file_up_down_loader import excel_file_uploader, excel_downloader
from components.replace_get_custom_info import replace_custom_info, get_custom_info


# 页面布局
st.title("服装规格信息提取")

# 获取文件并展示数据预览
file, data = excel_file_uploader()

# 读取关键词对应信息并打印
style_match_dict = get_match_dict("data/服装规格信息提取/款式.json")
size_match_dict = get_match_dict("data/服装规格信息提取/尺码.json")
color_match_dict = get_match_dict("data/服装规格信息提取/衣服颜色.json")

# 打印关键词信息，便于查验是否需要补充，如果需要补充，手动输入进行补充
style_tab, size_tab, color_tab, add_new_tab = st.tabs(["款式对应关系", "尺码对应关系", "颜色对应关系", "新增对应关系"])
with style_tab:
    st.subheader("款式对应关系")
    st.json(style_match_dict, expanded=False)
with size_tab:
    st.subheader("尺码对应关系")
    st.json(size_match_dict, expanded=False)
with color_tab:
    st.subheader("颜色对应关系")
    st.json(color_match_dict, expanded=False)
with add_new_tab:
    st.subheader("新增对应关系")
    selected_kind = st.selectbox("选择类型", ["款式对应关系", "尺码对应关系", "颜色对应关系"])
    english_key, chinese_value = st.columns(2, vertical_alignment="center")
    with english_key:
        filled_key = st.text_input("英文表述")
    with chinese_value:
        filled_value = st.text_input("中文表述")

    if selected_kind == "款式对应关系":
        # 规则可行性检查
        check_info = rule_check(filled_key, style_match_dict)

        if check_info == "规则可行性检查：OK":
            rule_add(filled_key, filled_value, style_match_dict, "data/服装规格信息提取/款式.json")

    if selected_kind == "尺码对应关系":
        # 规则可行性检查
        check_info = rule_check(filled_key, size_match_dict)

        if check_info == "规则可行性检查：OK":
            rule_add(filled_key, filled_value, size_match_dict, "data/服装规格信息提取/尺码.json")

    if selected_kind == "颜色对应关系":
        # 规则可行性检查
        check_info = rule_check(filled_key, color_match_dict)

        if check_info == "规则可行性检查：OK":
            rule_add(filled_key, filled_value, color_match_dict, "data/服装规格信息提取/衣服颜色.json")


# 处理完的结果提供下载链接
st.divider()
if file is not None:
    # 分别对衣服的款式、尺码和颜色进行检查并替换关键词
    for match_dict in [style_match_dict, size_match_dict, color_match_dict]:
        data["定制属性"] = data["定制属性"].apply(lambda x: replace_custom_info(x, match_dict))
    # 将衣服款式、尺码和颜色信息提取成列
    for title in ["款式", "尺码", "衣服颜色"]:
        data[title] = data["定制属性"].apply(lambda x: get_custom_info(x, title))
    excel_downloader(data, "服装规格信息提取结果")