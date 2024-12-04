import io

import streamlit as st
import pandas as pd

from components.json_read_write import get_match_dict, update_match_dict
from components.rule_check import rule_check


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
file = st.file_uploader("选择Excel文件", type="xlsx")
if file is not None:
    sheet_names = pd.read_excel(file, sheet_name=None)
    sheet_name = st.selectbox("选择表格", sheet_names)
    st.header("数据预览")
    data = sheet_names[sheet_name]
    st.dataframe(data, hide_index=True)
else:
    pass

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
            click_button = st.button("确认添加")
            if click_button:
                row_match_dict[filled_key] = "\r"
                update_match_dict("data/定制信息文本替换/整行替换规则.json", row_match_dict)

    if selected_kind == "标题替换":
        english_key, chinese_value = st.columns(2, vertical_alignment="center")
        with english_key:
            filled_key = st.text_input("输入需要替换的英文")
        with chinese_value:
            filled_value = st.text_input("输入对应的中文翻译")

        # 规则可行性检查
        check_info = rule_check(filled_key, key_match_dict)

        if check_info == "规则可行性检查：OK":
            click_button = st.button("确认添加")
            if click_button:
                key_match_dict[filled_key] = filled_value
                update_match_dict("data/定制信息文本替换/标题替换规则.json", key_match_dict)
                st.success("添加成功")


# 处理完的结果提供下载链接
st.divider()
if file is not None:
    data["定制属性"] = data["定制属性"].apply(lambda x: main(x, row_match_dict, key_match_dict))

    buffer = io.BytesIO()  # 初始化结果保存的内存空间

    # 将结果保存到 Excel 文件中
    with pd.ExcelWriter(buffer) as writer:
        data.to_excel(writer, sheet_name="处理后定制信息", index=False)
        writer.close()

        st.download_button(label="下载处理好的Excel表格", data=buffer, file_name="替换后定制信息表格.xlsx", mime="application/vnd.ms-excel")
        st.subheader("注意：将原本的表格移动到输出的文件内，图片单元格就能正常显示")
