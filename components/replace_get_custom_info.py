# 逐行遍历定制信息，整行内容与规则一致的进行替换
def replace_custom_info(x, dict_info):
    x_formated = x.replace("\r\n", "\r").replace("\n", "\r")  # 统一分隔符
    x_split_list = x_formated.split("\r")  # 根据分隔符拆分每行定制信息

    return_x_list = []  # 每行定制信息处理后列表
    for _x in x_split_list:
        return_x = _x.strip()  # 默认返回未替换的定制信息
        # 检查整行定制信息是否与规则一致，如果一致则进行替换
        if return_x in dict_info.keys():
            return_x = dict_info[return_x]
        return_x_list.append(return_x)  # 每行处理后结果列表，用于恢复原本的定制信息格式

    return "\r".join(return_x_list)  # 按原先的格式重构定制信息


# 将特定定制信息提取成列
def get_custom_info(x, key_word):
    x_list = x.split("\r")  # 定制信息逐行拆分
    result_list = []  # 返回结果列表
    for _x in x_list:
        if key_word in _x:
            result_list.append(_x)  # 逐行检查是否包含特定关键词

    # 根据关键词匹配结果，返回不同值
    if len(result_list) == 0:
        return None
    elif len(result_list) == 1:
        return result_list[0]
    elif len(result_list) > 1:
        return "\r".join(result_list)
