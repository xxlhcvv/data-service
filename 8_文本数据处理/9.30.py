# -*- coding: utf-8 -*-
"""
文本数据处理第一步：读取旅游评论语料 comment.txt
需要库：无（只用 Python 自带功能）
数据文件：comment.txt（一行一条评论）、stopwords.txt（停用词表，任务三用）
"""

# 导入 sys 模块，用于修改终端输出编码
import sys

# Windows 命令行默认 GBK 编码，打印中文内容时可能报错，改成 utf-8 更稳妥
sys.stdout.reconfigure(encoding='utf-8')

# 语料文件名（相对路径，表示和本 .py 文件放在同一个目录）
corpus_file = 'comment.txt'

# 1. 打开语料文件，把每一行读成一个元素放进列表
#    encoding='utf-8' 指定编码，保证中文正常读取
#    line.strip() 去掉每行末尾的换行符
#    if line.strip() 跳过空行
with open(corpus_file, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

# 2. 打印评论条数：len(lines) 求列表长度，即一共有多少条评论
print('共读取评论条数：', len(lines))

# 3. 统计文本总字数：sum(...) 把每条评论的长度加起来
total_chars = sum(len(line) for line in lines)
print('文本总字数：', total_chars)

# 4. 打印前 3 条，肉眼看一眼数据长什么样
print('\n前 3 条评论：')
for i, line in enumerate(lines[:3], 1):
    print(i, '→', line)

# =========================================================
# 下面新增：中文分词——三种模式对比
# =========================================================

# 导入 jieba（Python 里最常用的中文分词库）
import jieba

# 待分词的句子（经典例句：三种模式的差别在这句话上一眼就能看出来）
sentence = '我来到北京清华大学'

# 说明：jieba 的原始接口是 cut()，返回的是一个"生成器"（generator）

# 1. 精确模式：最准确地切，不重复、不遗漏，适合文本分析（最常用）
seg1 = list(jieba.cut(sentence))
print('精确模式　：', seg1)

# 2. 全模式：把句子里所有能成词的组合都扫出来，速度快但冗余多
seg2 = list(jieba.cut(sentence, cut_all=True))
print('全模式　　：', seg2)

# 3. 搜索引擎模式：在精确模式基础上把长词再切开，适合搜索引擎建索引
seg3 = list(jieba.cut_for_search(sentence))
print('搜索引擎模式：', seg3)

# =========================================================
# 下面新增：自定义词典——教 jieba 认识景区专有名词
# =========================================================

# 1. 先看不加自定义词时，这句话会被切成什么样
#    文件保存时一定要选 UTF-8 编码，否则脚本被当成本地 GBK 读取，中文会变乱码
s = '瑞金共和国摇篮景区，红井景区值得一游'
print('未加自定义词：', list(jieba.cut(s)))

# 2. add_word() 把专有名词写进 jieba 的词典
#    作用：告诉 jieba「这几个字要当成一个完整的词，不要拆开」
#    add_word() 的签名是：
#         add_word(word, freq, tag)
#      其中 freq 是【必填】参数（没有默认值），不传就会报
#         TypeError: add_word() missing 1 required positional argument: 'freq'
#      所以词频必须自己写一个数：数值越大，这个词越"容易被单独切出来"，
#      一般给个比较大的数（如 100000）就足够让它稳定成词了
jieba.add_word('共和国摇篮', 100000)
jieba.add_word('红井景区', 100000)

# 3. 再切一次，对比效果
#    加词之后，"共和国摇篮"、"红井景区" 会作为整体出现，不再被拆碎
print('加自定义词后：', list(jieba.cut(s)))

# =========================================================
# 下面新增：停用词过滤——先拿一句话试试
# =========================================================

# 1. 读入停用词表，用 set（集合）来存
#    集合查一个词在不在是"一步到位"，比列表快得多
with open('stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = {line.strip() for line in f if line.strip()}


# 2. 打印停用词表里有多少个词
#    ★ 注意：集合会自动去重！stopwords.txt 里其实有 209 行，
#      但因为 "还是""就是""真的" 等词重复出现，去重后 len() 会小于 209
print('停用词表大小（去重后）：', len(stopwords))

# 3. 拿一句话的分词结果试一试过滤效果
#    同样把 jieba.lcut 换成 list(jieba.cut(...))（当前 jieba 版本没有 lcut）
demo_words = list(jieba.cut('这个景区真的很不错，值得一游'))

# 4. 列表推导式做过滤：遍历每个词，只留下"不在停用词表里"的词
#    w not in stopwords：利用集合的 in 判断，速度很快
kept = [w for w in demo_words if w not in stopwords]

# 过滤前包含 "这个""真的""很""不错""值得" 等无实义词
print('过滤前：', demo_words)

# 过滤后这些词都被删掉，只留下有实际意义的词
print('过滤后：', kept)

# =========================================================
# 下面新增：停用词过滤——对全部评论
# =========================================================

# 导入 re 模块（正则表达式），Python 自带，用来判断一个词是不是纯中文
import re

# 1. 准备两个列表：过滤前的所有词、过滤后的有用词
all_words = []
clean_words = []

# 2. 逐条评论处理
for line in lines:
    for w in list(jieba.cut(line)):
        all_words.append(w)
        # 三个条件同时满足才留下：
        # ① 不在停用词表里  ② 至少 2 个字（去掉单字）  ③ 全是汉字（去掉标点/数字/英文）
        if w not in stopwords and len(w) >= 2 and re.fullmatch(r'[\u4e00-\u9fa5]+', w):
            clean_words.append(w)

print('过滤前总词数：', len(all_words))
print('过滤后总词数：', len(clean_words))

# =========================================================
# 下面新增：词频统计——找出游客最常提到什么
# =========================================================

# 从 collections 导入 Counter（计数器），Python 自带，无需安装
from collections import Counter

# 1. 把干净词库直接交给 Counter，一行完成统计
counter = Counter(clean_words)

# 2. len(counter) 是不重复词的个数
print('\n不重复词数：', len(counter))

# 3. most_common(20) 直接给出出现次数最多的前 20 个词
#    返回的是 [(词, 次数), (词, 次数), ...] 这样的列表
top20 = counter.most_common(20)
print('\n高频词 TOP20：')

# 4. enumerate(列表, 1) 从 1 开始编号，正好当排名用
for rank, (word, count) in enumerate(top20, 1):
    print(f'{rank:2d}. {word}  {count}')


# =========================================================
# 下面新增：把 TOP20 画成条形图
# =========================================================

# 导入 matplotlib 画图库
import matplotlib.pyplot as plt

# 让图表能显示中文：默认字体不支持中文，会显示成方块"□"
plt.rcParams['font.sans-serif'] = ['SimHei']

# 解决坐标轴负号 '-' 显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 1. 把 (词, 次数) 拆成两个列表，并倒序——barh 从下往上画，
#    倒序之后，次数最多的"景区"才会出现在最上面
words = [w for w, c in top20][::-1]
counts = [c for w, c in top20][::-1]

# 2. 画横向条形图（barh：h 是 horizontal 横向的意思）
plt.figure(figsize=(8, 6))
plt.barh(words, counts, color='#c00000')

# 3. 加标题和坐标轴说明
plt.title('评论高频词 TOP20')
plt.xlabel('出现次数')

# 4. tight_layout 自动排版，防止文字被裁掉
plt.tight_layout()

# 5. 保存成图片文件 + 弹窗显示
plt.savefig('top20_words.png', dpi=150)
plt.show()

# 6. 打印完成提示
print('\n已保存 top20_words.png')

