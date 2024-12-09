import streamlit as st
import pandas as pd

from components.json_read_write import get_match_dict
from components.rule_check_add import rule_check, rule_add
from components.file_up_down_loader import excel_file_uploader, excel_downloader


# 获取示例数据，写入缓存不更新
@st.cache_data
def get_example():
    return pd.read_excel("data/宠物陶瓷球/宠物陶瓷球实例数据.xlsx")

# 字符串内容替换
def string_replace(string, trans_dict):
    for key, value in trans_dict.items():
        string = string.replace(key, value)
    return string

# 定制属性整理
def custom_info_check(x, name_translate_dict, year_translate_dict):
    x_name_translated = string_replace(x, name_translate_dict)
    x_translated = string_replace(x_name_translated, year_translate_dict)
    return x_translated

# 添加图片顺序
def append_pic_num(x):
    pic_list = x.split("\r\n")
    pic_nums = len(pic_list)
    x_append = "\r\n".join([f"第{i}张图：{pic_list[i-1]}" for i in range(1, pic_nums+1)])
    return x_append

# 所需数据提取
def get_custom_info(x, start_title):
    x = x.replace("\r\n", "\n")
    x = x.replace("\r", "\n")
    x = x.split("\n")

    num = len(x)
    count = 0
    result = ""
    while count < num:
        if start_title in x[count]:
            result = x[count]
            count += 1
        else:
            count += 1
    return result

# 定制项字段规整
def custom_column_check(target_data, title, keyword):
    tmp_data = pd.DataFrame(index=target_data.index)
    for _ in title:
        tmp_data[_] = target_data[keyword].apply(lambda x: get_custom_info(x, _))
    tmp_data_stacked = tmp_data.stack()
    tmp_data_stacked = tmp_data_stacked.reset_index(level=-1, drop=True)
    return tmp_data_stacked

# 数据整理操作
def main(source_data, name_translate_dict, year_translate_dict, keep_columns=None):
    if keep_columns is None:
        keep_columns = ["订单图片", "数量", "订单号", "二维码", "二维码ID"]  # 必须保留的索引列
    keep_columns_plus_before = keep_columns.copy()  # 复制用于存储扩展字段
    keep_columns_plus_before.extend(["定制属性", "用户图片地址"])  # 扩展字段
    source_data = source_data.loc[:, keep_columns_plus_before]  # 保留需要的列

    # 定制信息整理
    source_data["翻译后定制信息"] = (source_data["定制属性"].
                                     apply(lambda x: custom_info_check(x, name_translate_dict, year_translate_dict)))
    source_data["添加序号的图片链接"] = source_data["用户图片地址"].apply(append_pic_num)

    # 输出字段整理
    name_title = [value for value in name_translate_dict.values()]
    year_title = [value for value in year_translate_dict.values()]
    pic_titles = [f"第{i}张图" for i in range(1, 10)]

    # 调整表格索引，便于结果汇总
    keep_columns_plus_after = keep_columns.copy()
    keep_columns_plus_after.extend(["翻译后定制信息", "添加序号的图片链接"])
    target_data = source_data.loc[:, keep_columns_plus_after]
    target_data.set_index(keep_columns, drop=True, inplace=True)

    # 规整表格
    name_df = custom_column_check(target_data, name_title, "翻译后定制信息")
    year_df = custom_column_check(target_data, year_title, "翻译后定制信息")
    pic_df = custom_column_check(target_data, pic_titles, "添加序号的图片链接")

    result_df = pd.concat([name_df, year_df, pic_df], ignore_index=False, axis=1)
    result_df.columns = ["名字信息", "年份信息", "图片信息"]
    result_df = result_df[result_df["图片信息"] != ""]
    result_df["名字信息"] = result_df["名字信息"].apply(lambda x: ("名字：" + (x.split(":")[1]).strip()) if x != "" else "")
    result_df["年份信息"] = result_df["年份信息"].apply(lambda x: ("年份：" + (x.split(":")[1]).strip()) if x != "" else "")
    result_df["图片信息"] = result_df["图片信息"].apply(lambda x: x.split("：")[1])
    result_df.reset_index(inplace=True)

    return result_df


# 页面布局
st.title("宠物陶瓷球定制信息整理")

# 获取文件并展示数据预览
file, data = excel_file_uploader()
if file is None:
    example = get_example()
    st.header("示例数据预览")
    st.dataframe(example, hide_index=True)


# 读取关键词对应信息并打印
name_match_dict = get_match_dict("data/宠物陶瓷球/名字关键词对应.json")
year_match_dict = get_match_dict("data/宠物陶瓷球/年份关键词对应.json")

# 打印关键词信息，便于查验是否需要补充，如果需要补充，手动输入进行补充
name_tab, year_tab, add_new_tab = st.tabs(["名字关键词", "年份关键词", "新增关键词"])
with name_tab:
    st.subheader("名字关键词对应关系")
    st.json(name_match_dict)
with year_tab:
    st.subheader("年份关键词对应关系")
    st.json(year_match_dict)
with add_new_tab:
    st.subheader("新增关键词对应关系")
    selected_kind = st.selectbox("关键词类型", ["名字关键词", "年份关键词"])
    english_key, chinese_value = st.columns(2, vertical_alignment="center")
    with english_key:
        filled_key = st.text_input("输入英文关键词")
    with chinese_value:
        filled_value = st.text_input("输入对应的中文关键词")

    # 规则可行性检查
    if selected_kind == "名字关键词":
        check_info = rule_check(filled_key, name_match_dict)

        if check_info == "规则可行性检查：OK":
            rule_add(filled_key, filled_value, name_match_dict, "data/宠物陶瓷球/名字关键词对应.json")

    elif selected_kind == "年份关键词":
        check_info = rule_check(filled_key, year_match_dict)

        if check_info == "规则可行性检查：OK":
            rule_add(filled_key, filled_value, year_match_dict, "data/宠物陶瓷球/年份关键词对应.json")


# 处理完的结果提供下载链接
st.divider()
if file is not None:
    output_data = main(data, name_match_dict, year_match_dict)  # 处理完成的表格
    excel_downloader(output_data, "处理后的宠物陶瓷球表格")
