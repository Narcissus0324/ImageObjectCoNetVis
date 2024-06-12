import json

# 定义读取和写入文件路径的列表
read_json_paths = [
    'comment_data/target_comment_seed2021.json',
    'comment_data/target_comment_no_image.json',
    'comment_data/20220128sample_comment.json',
]
write_json_paths = [
    'result/data/target_comment_seed2021.json',
    'result/data/target_comment_no_image.json',
    'result/data/20220128sample_comment.json',
]

# 循环处理每个文件
for read_path, write_path in zip(read_json_paths, write_json_paths):
    with open(read_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        # 处理字典中的每个键，每个键的值也是一个字典
        subset = {}
        for key, nested_dict in data.items():
            if isinstance(nested_dict, dict):
                # 选取嵌套字典中的前三个键值对
                selected_items = list(nested_dict.items())[:3]
                subset[key] = dict(selected_items)
            else:
                # 如果不是字典，则直接保留原始值
                subset[key] = nested_dict

    with open(write_path, 'w', encoding='utf-8') as outfile:
        json.dump(subset, outfile, indent=4, ensure_ascii=False)
