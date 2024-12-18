import streamlit as st

from components.json_read_write import get_match_dict
from components.rule_check_add import rule_add
from components.file_up_down_loader import excel_file_uploader, excel_downloader
from components.replace_get_custom_info import replace_custom_info, get_custom_info


# 页面布局
st.title("玩具汽车车型提取")

# 获取文件并展示数据预览
file, data = excel_file_uploader()

# 读取关键词对应信息并打印
match_dict = get_match_dict("data/玩具汽车/车型对应关系.json")

# 打印关键词信息，便于查验是否需要补充，如果需要补充，手动输入进行补充
style_tab, add_new_tab = st.tabs(["款式对应关系", "新增对应关系"])
with style_tab:
    st.subheader("款式对应关系")
    st.json(match_dict, expanded=False)
with add_new_tab:
    st.subheader("新增对应关系")
    english_key, chinese_value = st.columns(2, vertical_alignment="center")
    with english_key:
        filled_key = st.text_input("英文表述")
    with chinese_value:
        filled_value = st.text_input("中文表述")

    rule_add(filled_key, filled_value, match_dict, "data/玩具汽车/车型对应关系.json")


# 处理完的结果提供下载链接
st.divider()
if file is not None:
    data["定制属性"] = data["定制属性"].apply(lambda x: replace_custom_info(x, match_dict))
    data["车型"] = data["定制属性"].apply(lambda x: get_custom_info(x, "车型"))
    excel_downloader(data, "玩具汽车车型提取结果")
