import streamlit as st

from components.json_read_write import update_match_dict


# 添加规则时检查是否与已有规则存在包含关系
def rule_check(filled_key, check_dict):
    check_info = "规则可行性检查：OK"
    for cur_key in check_dict.keys():
        if filled_key in cur_key:
            check_info = f"新添加的规则 {filled_key} 被已有规则 {cur_key} 包含"
        elif cur_key in filled_key:
            check_info = f"新添加的规则 {filled_key} 将包含已有规则 {cur_key}"
    if check_info == "规则可行性检查：OK":
        st.success("可以添加")
    else:
        st.error(check_info)

    return check_info


# 将可以添加的规则加入规则字典中，并复写规则JSON文件
def rule_add(filled_key, filled_value, target_dict, target_file_path):
    click_button = st.button("确认添加")
    if click_button:
        target_dict[filled_key] = filled_value
        update_match_dict(target_file_path, target_dict)
        st.success("添加成功")
