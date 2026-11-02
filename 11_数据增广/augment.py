# -*- coding: utf-8 -*-
"""
图像增广（一）：回顾旋转与灰度
需要库：opencv-python、numpy
数据文件夹：data（存放 img（1）~ img（5）.jpg）
说明：旋转、灰度第 6 次课已学，本课合并成一段，快速生成增广样本；
     用 imdecode 绕开 Windows 中文/全角括号路径问题
"""

# 导入 sys 模块，用于修改终端输出编码
import sys

# Windows 命令行默认 GBK 编码，改成 utf-8 更稳妥
sys.stdout.reconfigure(encoding='utf-8')

# 导入 os 模块，用于遍历文件夹、拼接路径
import os

# 导入 numpy，用于把图片文件读成字节数组
import numpy as np

# 导入 opencv（导入名是 cv2）
import cv2

# 目标文件夹（图片都放在这个文件夹里）
data_dir = 'images'

# 自定义读图函数：先按字节读文件，再解码成图像数组
# 好处：中文/全角括号路径也能正常读（cv2.imread 对这类路径会读成 None）
def imread_cn(path, flags=cv2.IMREAD_COLOR):
    buf = np.fromfile(path, dtype=np.uint8)      # 把文件读成 uint8 字节数组
    return cv2.imdecode(buf, flags)              # 把字节数组解码成图像

# 自定义写图函数：先编码成图片字节，再写文件
def imwrite_cn(path, img):
    ext = os.path.splitext(path)[1]              # 取扩展名，如 .jpg
    cv2.imencode(ext, img)[1].tofile(path)       # 编码后写入（同样支持中文路径）

# 只挑出"原图"（排除已生成的 rotated_/_gray/_cropped 结果图），并排序
orig_files = sorted([f for f in os.listdir(data_dir)
                     if f.lower().endswith(('.jpg', '.png', '.jpeg'))
                     and not f.startswith('rotated_') and '_gray' not in f and '_cropped' not in f])
print('原图数量：', len(orig_files))
print('原图列表：', orig_files)

# =========================================================
# 1. 旋转 45 度（第 6 课：getRotationMatrix2D + warpAffine）
# =========================================================
for filename in orig_files:
    img = imread_cn(os.path.join(data_dir, filename))   # 读原图
    h, w = img.shape[:2]                                 # 取高、宽
    center = (w // 2, h // 2)                            # 旋转中心 = 图像正中心
    # 计算旋转矩阵：旋转中心、旋转角度 45、缩放因子 1.0
    M = cv2.getRotationMatrix2D(center, 45, 1.0)
    # 执行仿射变换，输出尺寸保持 宽×高 不变
    rotated = cv2.warpAffine(img, M, (w, h))
    # 新文件名加前缀 rotated_ 与原图区分
    imwrite_cn(os.path.join(data_dir, 'rotated_' + filename), rotated)
    print('旋转：', filename, '->', 'rotated_' + filename)

# =========================================================
# 2. 灰度（第 6 课：cvtColor 转 GRAY）——原图和旋转图都转一遍
# =========================================================
for filename in orig_files + ['rotated_' + f for f in orig_files]:
    img = imread_cn(os.path.join(data_dir, filename))   # 读彩色图
    # cvtColor 做颜色空间转换：BGR 彩色 -> GRAY 灰度（单通道）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    base, ext = os.path.splitext(filename)               # 拆出主名和扩展名
    imwrite_cn(os.path.join(data_dir, f'{base}_gray{ext}'), gray)
    print('灰度：', filename, '->', f'{base}_gray{ext}')

# =========================================================
# 任务一：图像裁剪（从左上角裁出 1/2 宽 × 1/2 高）
# =========================================================
def calculate_crop_dimensions(h, w):
    # 返回裁剪区域 (起点x, 起点y, 裁剪宽, 裁剪高)
    return (0, 0, w // 2, h // 2)                    # // 整除，保证是整数

def crop_image(image):
    h, w = image.shape[:2]                            # 取高、宽
    c = calculate_crop_dimensions(h, w)              # (x, y, cw, ch)
    # 数组切片：行取 [y : y+ch]，列取 [x : x+cw]
    return image[c[1]:c[1] + c[3], c[0]:c[0] + c[2]]

for filename in orig_files:
    img = imread_cn(os.path.join(data_dir, filename))    # 读原图
    cropped = crop_image(img)                            # 裁剪
    base, ext = os.path.splitext(filename)
    new_name = f'{base}_cropped{ext}'                     # 主名后加 _cropped
    imwrite_cn(os.path.join(data_dir, new_name), cropped)
    # 打印裁剪前后的尺寸对比，验证确实变成一半
    print(f'{filename}  {img.shape[1]}x{img.shape[0]}  ->  {new_name}  {cropped.shape[1]}x{cropped.shape[0]}')

# =========================================================
# 任务二：文本增广（同义词替换）
# =========================================================
# 导入 jieba（中文分词库）
import jieba
# 导入 Word2Vec（把词/句训练成向量的模型）
from gensim.models import Word2Vec
# 导入余弦相似度计算函数
from sklearn.metrics.pairwise import cosine_similarity

txt_dir = 'txt_data'

# ---- 1. 读取 5 个句子 ----
contents = []
with open(os.path.join(txt_dir, 'sentence.txt'), 'r', encoding='utf-8') as file:
    content = file.read()
    contents = [x for x in content.split('\n') if x.strip()]   # 按换行拆分，跳过空行
print('句子条数：', len(contents))
print(contents)

# ---- 2. 读取同义词组（每行一组，词之间空格分隔）----
synonym_list = []
with open(os.path.join(txt_dir, 'synonym.txt'), 'r', encoding='utf-8') as file:
    content = file.read()
    for i in content.split('\n'):
        if i.strip():
            synonym_list.append(i.split())       # split() 默认按空格拆成列表
print('同义词组数：', len(synonym_list))

# ---- 3. 对每个句子做同义词替换，生成所有替换版本 ----
augmented_data = []                              # 存放每个句子的所有增广结果
for sentence in contents:
    phrase = list(jieba.cut(sentence))                 # 分词，得到词语列表
    augmenting_sentences = []
    id1 = []                                     # 记录被替换词在句子中的位置
    id2 = []                                     # 记录命中的同义词组编号
    for p in phrase:
        for synonym in synonym_list:
            if p in synonym:                     # 这个词出现在某组同义词里
                id2.append(synonym_list.index(synonym))
                id1.append(phrase.index(p))
    for id in range(len(id1)):
        for synonym in synonym_list[id2[id]][1:]:  # [1:] 跳过第一个（原词自己）
            phrase[id1[id]] = synonym              # 把该位置换成同义词
            augmenting_sentences.append(''.join(phrase))  # 拼回整句
    augmented_data.append(augmenting_sentences)
print('\n第1句的增广结果（同义词替换）：')
for s in augmented_data[0]:
    print('   ', s)

# ---- 4. 训练 Word2Vec + 余弦相似度筛选 ----
def preprocess(sentences):
    # 把每个句子切成分词列表，供 Word2Vec 训练
    return [list(jieba.cut(sentence)) for sentence in sentences]

def sentence_vector(model, words):
    # 句子向量 = 句中所有"已知词"词向量的平均值
    words_known = [word for word in words if word in model.wv]
    if not words_known:
        return np.zeros(model.vector_size)       # 一个词都不认识，返回零向量
    vector = np.zeros(model.vector_size)
    for word in words_known:
        vector += model.wv[word]
    return vector / len(words_known)

tokenized_sentences = preprocess(contents)       # 分词
# 训练词向量模型：窗口5、最小词频1、4线程
model = Word2Vec(sentences=tokenized_sentences, window=5, min_count=1, workers=4)
print('\nWord2Vec 词向量维度：', model.vector_size)

# 把结果写入 augmentation_sentence.txt：原句 + 相似度≥0.8 的增广句
keep = 0
with open(os.path.join(txt_dir, 'augmentation_sentence.txt'), 'w', encoding='utf-8') as file:
    for id in range(len(contents)):
        sentence_1 = contents[id]
        file.write(sentence_1 + '\n')            # 先写原句
        keep += 1
        for sentence_2 in augmented_data[id]:
            v1 = sentence_vector(model, sentence_1)
            v2 = sentence_vector(model, sentence_2)
            sim = cosine_similarity([v1], [v2])[0][0]   # 计算两句的余弦相似度
            if sim >= 0.8:                                # 阈值 0.8，太低说明语义跑偏
                file.write(sentence_2 + '\n')
                keep += 1
print('同义词替换结果 augmentation_sentence.txt：', keep, '行')

# =========================================================
# 任务三：文本增广（句子重组）
# =========================================================
def reverse_from_comma_and_remove_period(s):
    # 目标：找到第一个逗号，把逗号前后两半交换，并把句号换成逗号
    comma_index = s.find('，')                    # 找第一个中文逗号的索引，找不到返回 -1
    if comma_index == -1:                          # 没有逗号
        return s.replace('。', '，')               # 直接把句号换成逗号返回
    before_comma = s[:comma_index]                 # 逗号前的内容
    after_comma = s[comma_index + 1:]              # 逗号后的内容（+1 跳过逗号本身）
    result = after_comma + before_comma            # 两半交换拼接
    return result.replace('。', '，')              # 句号统一换成逗号

with open(os.path.join(txt_dir, 'recombination_sentence.txt'), 'w', encoding='utf-8') as file:
    for i in contents:
        output_str = reverse_from_comma_and_remove_period(i)
        file.write(output_str + '\n')              # 每句写一行
        print('重组：', output_str)

