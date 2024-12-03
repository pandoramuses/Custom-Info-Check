import json

# 读取关键词对应表
def get_match_dict(filepath):
    with open(filepath, encoding="utf-8") as f:
        dict_info = json.load(f, strict=False)
    return dict_info

# 添加后的关键词对应表回写到文件，进行更新
def update_match_dict(filepath, dict_kind):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(json.dumps(dict_kind, indent=2, ensure_ascii=False))