import json

if __name__ == '__main__':
    result = {}
    comment_files = ["comment_data/20220128sample_comment.json",
                     "comment_data/target_comment_no_image.json",
                     "comment_data/target_comment_seed2021.json"]
    for comment_file in comment_files:
        print(f"Processing {comment_file}")
        with open(comment_file, 'r', encoding='utf-8') as f:
            comment = json.load(f)
        if 'pic_path' in comment:
            id_dict = comment['pic_path']
        else:
            print(f"Pic_path not in {comment_file}")
            continue
        for k in id_dict.keys():
            v = id_dict[k].split("\\")
            if len(v) >= 2:
                v = v[-2]
            else:
                v = ''
            id_dict[k] = v
        content_dict = comment['content']
        useful_dict = comment['usefulVoteCount']
        if id_dict.keys() == content_dict.keys():
            for cid, c_comment, c_useful in zip(id_dict.values(), content_dict.values(), useful_dict.values()):
                result[cid] = [c_comment, c_useful]
            print(f"Processed {comment_file}")
        else:
            print(f"Mismatch on {comment_file}")

    with open("comments_all.json", 'w', encoding='utf-8') as f:
        json.dump(result, f)


    with open("infer_result.json", 'r', encoding='utf-8') as f:
        infer = json.load(f)
    for item in infer.keys():
        for ccomment in infer[item].keys():
            infer[item][ccomment] = {
                "pic_reco": infer[item][ccomment],
                "comment": "" if ccomment not in result else result[ccomment][0],
                "useful": 0 if ccomment not in result else result[ccomment][1],
            }
    with open("infer+comment.json", 'w', encoding='utf-8') as f:
        json.dump(infer, f, ensure_ascii=False, indent=4)



