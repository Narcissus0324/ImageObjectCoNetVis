import os
import pickle
import random
from mmdet.apis import DetInferencer
from tqdm import tqdm

# random.seed(3407)

def pickle_dump(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def is_png(filename):    # 禁用png检测，因为存在一些png错误
    png_magic_number = b'\x89PNG\r\n\x1a\n'
    with open(filename, 'rb') as f:
        file_header = f.read(8)
    return file_header == png_magic_number

def is_jpg(filename):
    jpg_magic_number = b'\xff\xd8\xff'
    with open(filename, 'rb') as f:
        file_header = f.read(3)
    return file_header == jpg_magic_number

# 配置文件和检查点文件路径
config_file = 'code/rtmdet_tiny_8xb32-300e_coco.py'
checkpoint_file = 'code/rtmdet_tiny_8xb32-300e_coco_20220902_112414-78e30dcc.pth'

if __name__ == '__main__':
    # 创建推理器
    inferencer = DetInferencer(model=config_file,
                               weights=checkpoint_file,
                               device='cuda:0',
                               show_progress=True,)

    folder_dirs = []
    for i in range(1, 6):
        folder_dirs.append(f"./jd_comment_picture/pic_computer/{i}")
        folder_dirs.append(f"./jd_comment_picture/pic_data_high_pix/{i}")
        folder_dirs.append(f"./jd_comment_picture/pic_data_high_pix_downsample/{i}")

    img_path_dict = {}
    input_images = []
    for folder in folder_dirs:
        for item_id in os.listdir(folder):
            item_folder = f"{folder}/{item_id}"
            for comment_id in os.listdir(item_folder):
                comment_folder = f"{item_folder}/{comment_id}"
                for picture_name in os.listdir(comment_folder):
                    picture_dir = f"{comment_folder}/{picture_name}"
                    if is_jpg(picture_dir):
                        input_images.append(picture_dir)
                        img_path_dict[picture_dir] = (item_id, comment_id)

    # # 随机选择 5000 张图片
    # if len(input_images) > 5000:
    #     input_images = random.sample(input_images, 5000)
    pickle_dump(img_path_dict, 'img_path_dict.pkl')
    pickle_dump(input_images, 'input_image_dir_list.pkl')
    print(f"Valid Pictures: {len(input_images)}")

    all_results = []
    batch_size = 1000

    # 执行推理，按批处理，防止调度过大
    prog = tqdm(total=(len(input_images)+batch_size-1)//batch_size, desc="Batch Inference")
    for i in range((len(input_images)+batch_size-1)//batch_size):
        cur_batch_start = i * batch_size
        cur_batch_end = (i + 1) * batch_size
        result = inferencer(inputs=input_images[cur_batch_start:cur_batch_end],
                            out_dir='',
                            return_vis=False,
                            no_save_vis=True,
                            no_save_pred=True)
        for img_result in result['predictions']:
            all_results.append([])
            for score, label in zip(img_result['scores'], img_result['labels']):
                all_results[-1].append([score, label])
        if os.path.exists(f'all_results_{i-1}.pkl'):
            os.remove(f'all_results_{i-1}.pkl')
        pickle_dump(all_results, f'all_results_{i}.pkl')
        prog.update(1)
