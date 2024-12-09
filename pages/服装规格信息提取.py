import streamlit as st

from components.json_read_write import get_match_dict
from components.rule_check_add import rule_check, rule_add
from components.file_up_down_loader import excel_file_uploader, excel_downloader


# 逐行遍历定制信息，整行内容与规则一致的进行替换
def replace_custom_info(x):
    x_formated = x.replace("\r\n", "\r").replace("\n", "\r")  # 统一分隔符
    x_split_list = x_formated.split("\r")  # 根据分隔符拆分每行定制信息

    return_x_list = []  # 每行定制信息处理后列表
    for _x in x_split_list:
        _x_striped = _x.strip()  # 定制信息逐行处理，删去前后空格，以便和替换规则匹配
        return_x = _x_striped  # 默认返回未替换的定制信息
        # 检查整行定制信息是否与3项规则一致，如果一致则进行替换
        if _x_striped in style_match_dict.keys():
            return_x = style_match_dict[_x_striped]
        elif _x_striped in size_match_dict.keys():
            return_x = size_match_dict[_x_striped]
        elif _x_striped in color_match_dict.keys():
            return_x = size_match_dict[_x_striped]
        return_x_list.append(return_x)  # 每行处理后结果列表，用于恢复原本的定制信息格式

    return "\r".join(return_x_list)  # 按原先的格式重构定制信息


# 将服装的款式、尺码和颜色信息提取成列
def get_custom_info(x, key_word):
    x_list = x.split("\r")  # 定制信息逐行拆分
    result_list = []
    for _ in x_list:
        if key_word in _:
            result_list.append(_)

    # 根据关键词匹配结果，返回不同值
    if len(result_list) == 0:
        return None
    elif len(result_list) == 1:
        return result_list[0]
    elif len(result_list) > 1:
        return "\r".join(result_list)


# 页面布局
st.title("服装规格信息提取")

# 获取文件并展示数据预览
file, data = excel_file_uploader()

# 读取关键词对应信息并打印
style_match_dict = get_match_dict("data/服装规格信息提取/款式.json")
size_match_dict = get_match_dict("data/服装规格信息提取/尺码.json")
color_match_dict = get_match_dict("data/服装规格信息提取/颜色.json")

# 打印关键词信息，便于查验是否需要补充，如果需要补充，手动输入进行补充
style_tab, size_tab, color_tab, add_new_tab = st.tabs(["款式对应关系", "尺码对应关系", "颜色对应关系", "新增对应关系"])
with style_tab:
    st.subheader("款式对应关系")
    st.json(style_match_dict)
with size_tab:
    st.subheader("尺码对应关系")
    st.json(size_match_dict)
with color_tab:
    st.subheader("颜色对应关系")
    st.json(color_match_dict)
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
            rule_add(filled_key, filled_value, color_match_dict, "data/服装规格信息提取/颜色.json")


# 处理完的结果提供下载链接
st.divider()
if file is not None:
    for title in ["款式", "尺码", "颜色"]:
        data[title] = data["定制属性"].apply(lambda x: get_custom_info(x, title))
    excel_downloader(data, "服装规格信息提取结果")