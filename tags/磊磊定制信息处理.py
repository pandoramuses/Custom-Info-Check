import streamlit as st

from components.json_read_write import get_match_dict
from components.rule_check_add import rule_add
from components.file_up_down_loader import excel_file_uploader, excel_downloader


# 标题替换
def title_replace(x, replace_dict):
    x = x.replace("\r\n", "\r").replace("\n", "\r")  # 统一分隔符
    part_text_list = x.split("\r")  # 拆分每行定制信息
    replaced_parts = []  # 每行处理后的结果列表
    for part_text in part_text_list:  # 遍历每行定制信息
        replaced_text = part_text.strip()  # 删除多余空格
        custom_title = part_text.split(":")[0].strip()  # 标题信息删除多余空格
        custom_value = "".join(part_text.split(":")[1:]).strip()  # 值信息删除多余空格
        for key, value in replace_dict.items():  # 遍历规则字典
            if custom_title == key:  # 当标题信息在规则字典中
                replaced_text = ":".join([value, custom_value])  # 将替换后标题表述和原本值信息组合成输出结果
        replaced_parts.append(replaced_text)
    # 使用分隔符重新连接
    return "\r".join(replaced_parts)


# 根据标题整行删除
def title_row_replace(x, replace_dict):
    x = x.replace("\r\n", "\r").replace("\n", "\r")  # 统一分隔符
    part_text_list = x.split("\r")  # 拆分每行定制信息
    replaced_parts = []  # 每行处理后的结果列表
    for part_text in part_text_list:  # 遍历每行定制信息
        replaced_text = part_text.strip()  # 删除多余空格
        custom_title = part_text.split(":")[0]  # 以冒号作分割提取标题信息
        custom_title = custom_title.strip()  # 标题信息删除多余空格
        for key, value in replace_dict.items():  # 遍历规则字典
            if custom_title == key:  # 当标题信息在规则字典中
                replaced_text = "\r"  # 将整行定制信息删除
        replaced_parts.append(replaced_text)
    # 使用分隔符重新连接
    return "\r".join(replaced_parts)


# 整行替换
def row_replace(x, replace_dict):
    while "\r\r" in x:
        x = x.replace("\r\r", "\r")
    x = x.replace("\r\n", "\r").replace("\n", "\r")
    part_text_list = x.split("\r")
    replaced_parts = []
    for part_text in part_text_list:
        replaced_text = part_text.strip()
        for key, value in replace_dict.items():
            if key == replaced_text:  # 检查是否存在key，减少不必要的操作
                replaced_text = value
        replaced_parts.append(replaced_text)
    # 使用分隔符重新连接
    return "\r".join(replaced_parts)


# 最后处理多余的换行符
def multi_new_line_check(x):
    while "\r\r" in x:
        x = x.replace("\r\r", "\r")
    if x[0] == "\r":
        x[0] = ""
    if x[-1] == "\r":
        x[-1] = ""
    return x


# 页面布局
st.title("磊磊定制信息处理")

st.subheader("替换规则说明")
st.markdown(
    """
    1. **标题替换：仅替换定制标题文本表述【保留系统导出的英文冒号】**
        - 英文文本和中文表述都要填写

    | 原表述 | 替换后结果 |
    | :---: | :---: |
    | Choose Blanket Color : Black | 毛毯颜色:Black |
    | Song Title : Worst Way | 歌曲名:Worst Way |

    2. **标题整行替换：比对每行定制信息的标题是否与录入的规则标题一致，如果一致，整行删除**
        - 只需要输入英文文本

    | 原表述 | 最终结果 |
    | :---: | :---: |
    | Add VIP Service : No, thanks | 识别到规则关键词：Add VIP Service，整行删除 |
    | Add A Gift Card? : No, thanks | 识别到规则关键词：Add A Gift Card?，整行删除 |

    3. **整行替换：将定制信息中的某一整行替换成另一种表述【可以在替换时更改为任意分割符】。如果不输入中文表述，将默认进行整行删除的操作**
        - 只需要输入英文文本
    
    | 原表述 | 替换后结果 |
    | :---: | :---: |
    | Choose Blanket Color : Black | 毛毯颜色：黑色 |
    | Add VIP Service : No, thanks | 识别到没有添加对应表述，整行删除 |
    """
)
st.info("程序将按照：标题替换 -> 标题整行替换 -> 整行替换 的顺序处理，在添加规则时留意替换方式的选择！")
st.divider()

# 获取文件并展示数据预览
file, data = excel_file_uploader()

# 读取替换规则并输出
key_match_dict = get_match_dict("data/磊磊定制信息处理/标题替换规则.json")
key_row_match_dict = get_match_dict("data/磊磊定制信息处理/标题整行替换规则.json")
row_match_dict = get_match_dict("data/磊磊定制信息处理/整行替换规则.json")


# 打印关键词信息，便于查验是否需要补充，如果需要补充，手动输入进行补充
key_tab, key_row_tab, row_tab,  add_new_tab = st.tabs(["标题替换规则", "标题整行替换规则", "整行替换规则", "新增替换规则"])
with key_tab:
    st.subheader("标题替换规则")
    st.json(key_match_dict, expanded=False)
with key_row_tab:
    st.subheader("标题整行替换规则")
    st.json(key_row_match_dict, expanded=False)
with row_tab:
    st.subheader("整行替换规则")
    st.json(row_match_dict, expanded=False)
with add_new_tab:
    st.subheader("新增替换规则")
    mode = st.selectbox("替换方式", ["标题替换", "标题整行替换", "整行替换"])

    # 替换文本记录
    input_key, input_value = st.columns(2, vertical_alignment="center")
    with input_key:
        filled_key = st.text_input("输入需要替换的英文文本").strip()
    with input_value:
        filled_value = st.text_input("输入对应的中文表述").strip()

    # 根据替换模式，将新替换规则写入对应文件
    if mode == "标题替换":
        rule_add(filled_key, filled_value, key_match_dict, "data/磊磊定制信息处理/标题替换规则.json")

    if mode == "标题整行替换":
        rule_add(filled_key, "", key_row_match_dict, "data/磊磊定制信息处理/标题整行替换规则.json")

    if mode == "整行替换":
        if filled_value != "":
            rule_add(filled_key, filled_value, row_match_dict, "data/磊磊定制信息处理/整行替换规则.json")
        else:
            rule_add(filled_key, "\r", row_match_dict, "data/磊磊定制信息处理/整行替换规则.json")


# 处理完的结果提供下载链接
st.divider()
if file is not None:
    data["定制属性"] = data["定制属性"].apply(lambda x: title_replace(x, key_match_dict))
    data["定制属性"] = data["定制属性"].apply(lambda x: title_row_replace(x, key_row_match_dict))
    data["定制属性"] = data["定制属性"].apply(lambda x: row_replace(x, row_match_dict))
    data["定制属性"] = data["定制属性"].apply(multi_new_line_check)
    excel_downloader(data, "替换后定制信息表格")
