import streamlit as st

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