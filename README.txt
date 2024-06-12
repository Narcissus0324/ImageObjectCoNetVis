1、首先按顺序安装：
Python 3.9
Torch 2.1

2、然后安装requirement.txt的所有包

3、将图片数据解压，类似如下结构则解压正确
代码根目录\jd_comment_picture\pic_computer\1\1000054\10371673125\0.jpg

4、将评论数据（三个json）解压，类似如下结构则解压正确
代码根目录\comment_data\20220128sample_comment.json

5、运行代码顺序：
   1. inference.py，执行图像识别任务
   2. extract_word_class.py，导出图像类别
   3. extract_inference_result.py，导出图像推理结果到json（问题1）
   4. co_occurence.py，分析图像共现性（问题2）
   5. comment_json_parse.py，将评论json进行分析
   6. translate_recognition.py，将评论与图像识别结果匹配（问题3）

   其他py文件是依赖文件，请勿删除