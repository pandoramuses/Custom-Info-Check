import io

import pandas as pd
import streamlit as st


# 上传Excel文件并预览
def excel_file_uploader():
    file = st.file_uploader("选择Excel文件", type="xlsx")
    if file is not None:
        sheet_names = pd.read_excel(file, sheet_name=None)
        sheet_name = st.selectbox("选择表格", sheet_names)
        st.header("数据预览")
        data = sheet_names[sheet_name]
        st.dataframe(data, hide_index=True, use_container_width=True)
        return file, data
    else:
        return file, None


# Excel文件下载
def excel_downloader(data, file_name):
    buffer = io.BytesIO()  # 初始化结果保存的内存空间

    # 将结果保存到 Excel 文件中
    with pd.ExcelWriter(buffer) as writer:
        data.to_excel(writer, sheet_name=file_name, index=False)
        writer.close()

        st.download_button(label="下载处理好的Excel表格", data=buffer, file_name=f"{file_name}.xlsx", mime="application/vnd.ms-excel")
        st.subheader("注意：将原本的表格移动到输出的文件内，图片单元格就能正常显示")
