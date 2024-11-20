import io

import streamlit as st
import pandas as pd
from collections import Counter


# 检查表头信息
def column_check(data, count=0):
    columns = data.columns
    try:
        if "字母" not in columns:
            st.write("请确认所选表格中存在 '字母' 列")
            count += 1
    finally:
        pass

    try:
        if "字母颜色" not in columns:
            st.write("请确认所选表格中存在 '字母颜色' 列")
            count += 1
        else:
            data["判定"] = data["字母颜色"].apply(lambda x: 1 if "色" in x else 0)
            if data["判定"].sum() != len(data["判定"]):
                st.write("请确认所选表格中 '字母颜色' 列是正确的颜色信息")
                count += 1
    finally:
        pass

    try:
        for i in range(1, num + 1):
            if f"补丁{i}" not in columns:
                st.write(f"补丁{i}字段不在所选表格中，请确认最多补丁数量是否正确")
                count += 1
    finally:
        pass

    if count == 0:
        return 0
    else:
        return 1

# 计算各个颜色的字母贴片数量
def cal_char_num(data):
    char_list = []
    for item in data["字母"]:
        item_no_space = item.replace(" ", "")
        char_list.extend(list(item_no_space))  # 将每个字母拆开加入列表
    return Counter(char_list)


# 初始化结果保存的内存空间
buffer = io.BytesIO()

# 上传文件
file = st.file_uploader(label="选择Excel表格", type="xlsx")

# 若未上传文件，则不进行处理
if file is not None:
    filename = file.name

    # 读取文件工作表，并输出文件中有哪些表格
    df_list = pd.read_excel(file, sheet_name=None)
    sheet_names = df_list.keys()
    sheet_choice = st.selectbox(label="选择工作表", options=sheet_names)

    # 根据选择的表格，展示表格内容
    st.header("表格数据预览")
    show_df = st.dataframe(df_list[sheet_choice], hide_index=True)

    # 补丁数量记录
    num = st.number_input(label="最多一行的补丁数量", value=6)

    # 进行列字段检查
    check_state = column_check(df_list[sheet_choice])

    # 如果列字段无异常，进行汇总操作，否则不进行后续操作
    if not check_state:
        df_list[sheet_choice]["字母"] = df_list[sheet_choice]["字母"].apply(lambda x: x.upper() if pd.notna(x) else "")

        # 定义颜色列表，用于分表处理
        color_list = df_list[sheet_choice]["字母颜色"].unique()  # 可根据表格内颜色确定所需颜色
        color_sum = {}  # 存储各颜色字母的汇总结果

        # 遍历颜色列表，计算每种颜色的字母数量
        for color in color_list:
            color_data = df_list[sheet_choice][df_list[sheet_choice]["字母颜色"] == color]  # 按颜色筛选数据
            color_sum[f"{color}字母汇总"] = pd.Series(cal_char_num(color_data), name="数量").sort_values(ascending=False)

        # 提取图案列，并汇总图案数量
        tuan = df_list[sheet_choice].loc[:, [f"补丁{i}" for i in range(1, num + 1)]]  # 提取补丁1-6列
        tuan_list = tuan.values.flatten()  # 展平数据为一维列表
        tuan_list = [tuan for tuan in tuan_list if pd.notna(tuan)]  # 过滤空值
        tuan_sum = pd.Series(Counter(tuan_list), name="数量").sort_values(ascending=False)  # 统计每种图案的数量

        # 将结果保存到 Excel 文件中
        with pd.ExcelWriter(buffer) as writer:
            # 保存各颜色的字母汇总
            for color_name, summary in color_sum.items():
                summary.to_excel(writer, sheet_name=color_name)

            # 保存图案汇总结果
            tuan_sum.to_excel(writer, sheet_name="图案汇总")

            # 关闭文件
            writer.close()

            st.download_button(label="下载处理好的Excel表格", data=buffer, file_name="处理后的贴片信息.xlsx", mime="application/vnd.ms-excel")
            st.header("注意：将原本的表格移动到输出的文件内，补丁图标就能正常显示")
    else:
        pass
else:
    st.header("尚未选择文件")

