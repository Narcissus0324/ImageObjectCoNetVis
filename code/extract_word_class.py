import json

import torch

# 加载模型权重文件
checkpoint = torch.load('code/rtmdet_tiny_8xb32-300e_coco_20220902_112414-78e30dcc.pth', map_location='cpu')

with open("all_classes.json", 'w', encoding='utf-8') as f:
    json.dump(checkpoint['meta']['dataset_meta']['CLASSES'], f)
