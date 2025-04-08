import streamlit as st

from components.file_up_down_loader import excel_file_uploader, excel_downloader
from components.sql_option import database_connection, get_rules
from components.replace_get_custom_info import replace_custom_info, get_custom_info, format_rule_text


# 页面布局
st.title("定制信息提取")

# 获取文件并展示数据预览
file, data = excel_file_uploader()
if file is not None:
    if "定制属性" in data.columns:
        data["定制属性"] = data["定制属性"].fillna("无定制信息")


# 读取替换规则信息
rules = get_rules()

# 打印关键词信息，便于查验是否需要补充，如果需要补充，手动输入进行补充
search_tab, add_tab = st.tabs(["规则查询", "新增规则"])
with search_tab:
    type_select, rules_show = st.columns([1, 4], vertical_alignment="center")
    with type_select:
        rule_type = st.selectbox("选择要查询的商品分类", rules["类型"].unique())
        rule_title = st.multiselect("选择要查询的定制属性", rules[rules["类型"] == rule_type]["中文表述"].unique())
    with rules_show:
        if rule_title:
            st.dataframe(rules[(rules["类型"] == rule_type) & (rules["中文表述"].isin(rule_title))], use_container_width=True, hide_index=True)
        else:
            st.dataframe(rules[rules["类型"] == rule_type], use_container_width=True, hide_index=True)
with add_tab:
    goods_type, english_key, chinese_value = st.columns(3, vertical_alignment="center")
    with goods_type:
        type_name = st.text_input("商品类型").strip()
    with english_key:
        filled_key = st.text_input("英文定制标题").strip().lower()
        format_filled_key = format_rule_text(filled_key)
    with chinese_value:
        filled_value = st.text_input("中文定制标题").strip()

    # 规则写入数据库
    conn, cursor = database_connection()
    add_button = st.button(label="确认添加")
    if add_button:
        if (type_name == "") | (filled_key == "") | (filled_value == ""):
            st.error("添加的规则内容不全，请补充完整后再提交")
        else:
            if format_filled_key not in rules["英文表述"].unique():
                try:
                    cursor.execute("insert into rules (type, english, chinese) values (?, ?, ?)",
                                   params=(type_name, format_filled_key, filled_value))
                    conn.commit()
                except Exception as e:
                    st.error(f"规则添加失败：{e}")
                else:
                    st.success("添加成功")
                finally:
                    cursor.close()
                    conn.close()
            else:
                dul_rule = rules[(rules["英文表述"] == format_filled_key) & (rules["类型"] == type_name)]["中文表述"].tolist()
                if filled_value not in dul_rule:
                    try:
                        cursor.execute("insert into rules (type, english, chinese) values (?, ?, ?)",
                                       params=(type_name, format_filled_key, filled_value))
                        conn.commit()
                    except Exception as e:
                        st.error(f"规则添加失败：{e}")
                    else:
                        st.success("添加成功")
                    finally:
                        cursor.close()
                        conn.close()
                else:
                    st.error("对应定制信息已存在对应规则")


# 确认需要提取的字段
st.divider()
selected_types = st.selectbox("选择要提取的商品类型", rules["类型"].unique())
selected_title = st.multiselect("选择要提取的定制属性", rules[rules["类型"] == selected_types]["中文表述"].unique())


# 处理完的结果提供下载链接
if file is not None:
    # 按类型替换定制标题
    for title in selected_title:
        # 根据规则信息生成规则字典
        title_rules_dict = rules[(rules["类型"] == selected_types) & (rules["中文表述"] == title)].set_index("英文表述")["中文表述"].to_dict()
        data["替换后定制属性"] = data["定制属性"].apply(lambda x: replace_custom_info(x, title_rules_dict))
        data[title] = data["替换后定制属性"].apply(lambda x: get_custom_info(x, title))
        data.drop(columns="替换后定制属性", inplace=True)
    excel_downloader(data, "定制信息提取结果")
