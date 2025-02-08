import re

# 逐行遍历定制信息，整行内容与规则一致的进行替换
def replace_custom_info(x, dict_info, _split=True):
    x_formated = x.replace("\r\n", "\r").replace("\n", "\r")  # 统一分隔符
    x_formated = x_formated.replace("：", ":")  # 将中文冒号替换成英文冒号
    x_formated = x_formated.lower()  # 将定制信息统一改成小写，缩减比对字典
    x_split_list = x_formated.split("\r")  # 根据分隔符拆分每行定制信息

    return_x_list = []  # 每行定制信息处理后列表
    for _x in x_split_list:
        # 处理定制信息不规范导致的异常规则
        custom_name = _x.split(":")[0].strip()  # 定制标题
        custom_value = "".join(_x.split(":")[1:]).strip()  # 定制属性
        main_custom_name = "-".join([_.strip() for _ in custom_name.split("-") if re.match(r"^[0-9]+$", _.strip()) is None])  # 剔除重名定制标题，插件自动加的后缀
        _x = ":".join([main_custom_name, custom_value])  # 重组定制信息
        _x = _x.split("|")[0].strip()  # 剔除定制加钱金额部分，减少所需规则数量

        # 替换结果输出
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
        if key_word == _x.split("：")[0]:
            result_list.append(_x)  # 逐行检查是否包含特定关键词

    # 根据关键词匹配结果，返回不同值
    if len(result_list) == 0:
        return None
    elif len(result_list) == 1:
        return result_list[0]
    elif len(result_list) > 1:
        return "\r".join(result_list)


# 添加规则时将规则进行标准格式的处理
def format_rule_text(text):
    text = text.lower()  # 统一转为小写，便于比对
    name = text.split(":")[0].strip()  # 获取定制标题
    value = "".join(text.split(":")[1:]).strip()  # 获取定制属性值
    main_custom_name = "-".join([_.strip() for _ in name.split("-") if re.match(r"^[0-9]+$", _.strip()) is None])  # 剔除重名定制标题，插件自动加的后缀
    format_text = ":".join([main_custom_name, value])  # 重组定制信息
    format_text = format_text.split("|")[0].strip()  # 剔除定制加钱金额部分，减少所需规则数量
    return format_text
