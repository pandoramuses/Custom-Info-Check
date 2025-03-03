# 标题替换
def title_replace(x, replace_dict):
    x = x.replace("\r\n", "\r").replace("\n", "\r")  # 统一分隔符
    part_text_list = x.split("\r")  # 拆分每行定制信息
    replaced_parts = []  # 每行处理后的结果列表
    for part_text in part_text_list:  # 遍历每行定制信息
        replaced_text = part_text.split("|")[0].strip()  # 删除加价金额后删除多余空格
        custom_title = replaced_text.split(":")[0].split("-")[0].strip().lower()  # 标题信息删除多余空格并统一转为小写
        custom_value = "".join(replaced_text.split(":")[1:]).strip()  # 值信息删除多余空格
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


# 将特定定制信息提取成列
def get_custom_info(x, key_word):
    x_list = x.split("\r")  # 定制信息逐行拆分
    result_list = []  # 返回结果列表
    for _x in x_list:
        if key_word == _x.split(":")[0]:
            result_list.append(_x)  # 逐行检查是否包含特定关键词

    # 根据关键词匹配结果，返回不同值
    if len(result_list) == 0:
        return None
    elif len(result_list) == 1:
        return result_list[0]
    elif len(result_list) > 1:
        return "\r".join(result_list)
