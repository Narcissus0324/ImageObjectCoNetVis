from translate import translations
import json
from scipy.stats import pearsonr, spearmanr, kendalltau


if __name__ == '__main__':
    with open("infer+comment.json", 'r', encoding='utf-8') as f:
        comments = json.load(f)
    corrx = []
    corry = []
    for item_id in comments:
        for comment_id in comments[item_id]:
            comments[item_id][comment_id]['pic_text_score'] = 0
            keywords = set()
            for pic_reco_result in comments[item_id][comment_id]['pic_reco']:
                for translate in translations[pic_reco_result]:
                    keywords.add(translate)
            for keyword in keywords:
                comments[item_id][comment_id]['pic_text_score'] += \
                    comments[item_id][comment_id]['comment'].count(keyword)
            corrx.append(comments[item_id][comment_id]['pic_text_score'])
            corry.append(comments[item_id][comment_id]['useful'])
    with open("infer+comment+kw.json", 'w', encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=4)

    print("图文相关性 和 评论有用性 的相关系数：")

    # 计算皮尔逊相关系数
    pearson_corr, pearson_p_value = pearsonr(corrx, corry)
    print(f"皮尔逊相关系数: {pearson_corr}, p值: {pearson_p_value}")

    # 计算斯皮尔曼相关系数
    spearman_corr, spearman_p_value = spearmanr(corrx, corry)
    print(f"斯皮尔曼相关系数: {spearman_corr}, p值: {spearman_p_value}")

    # 计算肯德尔相关系数
    kendall_corr, kendall_p_value = kendalltau(corrx, corry)
    print(f"肯德尔相关系数: {kendall_corr}, p值: {kendall_p_value}")

