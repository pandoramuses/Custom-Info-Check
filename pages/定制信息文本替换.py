import streamlit as st

from components.json_read_write import get_match_dict
from components.rule_check_add import rule_check, rule_add
from components.file_up_down_loader import excel_file_uploader, excel_downloader


# 文本替换
def text_replace(x, replace_dict):
    x = x.replace("\r\n", "\r").replace("\n", "\r")
    part_text_list = x.split("\r")
    replaced_parts = []
    for part_text in part_text_list:
        replaced_text = part_text
        for key, value in replace_dict.items():
            if key in replaced_text:  # 检查是否存在key，减少不必要的操作
                replaced_text = replaced_text.replace(key, value)
        replaced_parts.append(replaced_text)
    # 使用分隔符重新连接
    return "\r".join(replaced_parts)

# 总替换函数，先整行替换，再标题替换
def main(x, row_replace_dict, title_replace_dict):
    row_replaced = text_replace(x, row_replace_dict)
    title_replaced = text_replace(row_replaced, title_replace_dict)
    return title_replaced


# 页面布局
st.title("定制信息文本替换")

# 获取文件并展示数据预览
file, data = excel_file_uploader()

# 读取关键词对应信息并打印
row_match_dict = get_match_dict("data/定制信息文本替换/整行替换规则.json")
key_match_dict = get_match_dict("data/定制信息文本替换/标题替换规则.json")

# 打印关键词信息，便于查验是否需要补充，如果需要补充，手动输入进行补充
row_tab, key_tab, add_new_tab = st.tabs(["整行替换规则", "标题替换规则", "新增替换规则"])
with row_tab:
    st.subheader("整行替换规则")
    st.json(row_match_dict)
with key_tab:
    st.subheader("标题替换规则")
    st.json(key_match_dict)
with add_new_tab:
    st.subheader("新增替换规则")
    selected_kind = st.selectbox("选择类型", ["整行替换", "标题替换"])
    if selected_kind == "整行替换":
        filled_key = st.text_input("输入需要替换的英文")

        # 规则可行性检查
        check_info = rule_check(filled_key, row_match_dict)

        if check_info == "规则可行性检查：OK":
            rule_add(filled_key, "\r", row_match_dict, "data/定制信息文本替换/整行替换规则.json")

    if selected_kind == "标题替换":
        english_key, chinese_value = st.columns(2, vertical_alignment="center")
        with english_key:
            filled_key = st.text_input("输入需要替换的英文")
        with chinese_value:
            filled_value = st.text_input("输入对应的中文翻译")

        # 规则可行性检查
        check_info = rule_check(filled_key, key_match_dict)

        if check_info == "规则可行性检查：OK":
            rule_add(filled_key, filled_value, key_match_dict, "data/定制信息文本替换/标题替换规则.json")


# 处理完的结果提供下载链接
st.divider()
if file is not None:
    data["定制属性"] = data["定制属性"].apply(lambda x: main(x, row_match_dict, key_match_dict))
    excel_downloader(data, "替换后定制信息表格")
