import json
import pickle
from tqdm import tqdm


def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


with open("all_classes.json", 'r', encoding='utf-8') as f:
    id_to_class = json.load(f)


if __name__ == '__main__':
    score_threshold = 0.25

    imgdict = load_pickle("img_path_dict.pkl")
    images = load_pickle("input_image_dir_list.pkl")
    inferences = load_pickle("all_results_113.pkl")

    # all_inference_confidence = []
    # for item in inferences:
    #     for score, _ in item:
    #         all_inference_confidence.append(score)

    # Percentiles:
    # len(all_inference) = 34130100
    # np.percentile(all_inference_confidence, 30)
    # 0.034146592020988464
    # np.percentile(all_inference_confidence, 50)  == saving 17065050 samples
    # 0.04432700201869011
    # np.percentile(all_inference_confidence, 90)
    # 0.10394527018070221
    # np.percentile(all_inference_confidence, 99)  == saving 341301 samples
    # 0.29562289535999087

    output_result = {}

    progbar = tqdm(total=len(images))

    for image, inference in zip(images, inferences):
        progbar.update(1)
        current_picture_items = set()
        for raw_score, raw_label in inference:
            if raw_score >= score_threshold:
                current_picture_items.add(raw_label)
        item_id, comment_id = imgdict[image]
        if item_id not in output_result:
            output_result[item_id] = {}
        if comment_id not in output_result[item_id]:
            output_result[item_id][comment_id] = set()
        for i in current_picture_items:
            output_result[item_id][comment_id].add(i)

    for item_id in output_result.keys():
        for comment_id in output_result[item_id].keys():
            output_result[item_id][comment_id] = list(map(lambda x: id_to_class[x],
                                                      list(output_result[item_id][comment_id])))
    with open("infer_result.json", 'w', encoding='utf-8') as f:
        json.dump(output_result, f, indent=4)
        # use indent=None for minimum size


