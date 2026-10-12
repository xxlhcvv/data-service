# -*- coding: utf-8 -*-
"""
像素级操作入门：读取 pic1.jpg，读取像素值、转灰度、截取 ROI
需要库：opencv-python
未安装可执行：pip install opencv-python
"""

# 导入 OpenCV 库，用于读取图片、颜色转换、切片截取
import cv2

# 导入 NumPy，用于 hstack 横向拼接对比图
import numpy as np

# 导入 sys 模块，用于修改终端输出编码
import sys

# Windows 命令行默认 GBK 编码，打印特殊字符时可能报错，改成 utf-8 更稳妥
sys.stdout.reconfigure(encoding='utf-8')

# 图片文件名（相对路径，表示在本 .py 文件所在的目录下找 pic1.jpg）
file_name = 'pic1.jpg'

# 1. 用 imread() 读取图片
#    读取成功：返回一个 numpy 数组（三维：高 × 宽 × 通道数）
#    读取失败：返回 None，不会报错，所以必须自己判断
img = cv2.imread(file_name)

# 2. 判断图片是否读取成功
if img is None:
    # 读取失败时打印提示和常见原因
    print('图片读取失败！常见原因：')
    print('1. 文件不在本 .py 文件的同一目录下（当前找不到', file_name, '）')
    print('2. 文件路径中含有中文，cv2.imread() 对中文路径支持不好')
    print('   解决办法：把图片移到英文路径下，或用 np.fromfile() + cv2.imdecode() 读取')
else:
    # 3. 打印图像的 shape
    #    shape 是 (高, 宽, 通道数)，例如 (2094, 1486, 3)
    #    说明：高 2094 行、宽 1486 列、每个像素 3 个颜色通道
    print('图像 shape（高, 宽, 通道数）:', img.shape)

    # 4. 读取 (50, 50) 位置的像素值
    #    写法是 img[行, 列]，也就是 img[y, x]
    #    第 1 个 50 是行号（从上往下数第 50 行，y 方向）
    #    第 2 个 50 是列号（从左往右数第 50 列，x 方向）
    #    注意不是 (x, y)，和数学里的坐标顺序相反
    pixel_50 = img[50, 50]

    # 打印左上角位置（白背景）的像素值
    #    返回 3 个数，顺序是 B（蓝）、G（绿）、R（红）
    #    白色背景三个值都接近 255，例如 [255 255 255]
    print('img[50, 50] 的像素值（左上角白背景）:', pixel_50)

    # 5. 读取 (1047, 743) 位置的像素值（鸭子身体）
    #    同样写法 img[行, 列]，行在前、列在后
    pixel_duck = img[1047, 743]

    # 打印鸭子身体位置的像素值，同样是 B、G、R 三个数
    print('img[1047, 743] 的像素值（鸭子身体）:', pixel_duck)

    # 6. 把 img[1047, 743] 拆包成 b、g、r 三个变量
    #    拆包（解包）：右边是 3 个数，左边写 3 个变量，按顺序一一对应赋值
    #    顺序仍然是 B、G、R，所以第 1 个给 b、第 2 个给 g、第 3 个给 r
    b, g, r = img[1047, 743]

    # 分别打印三个通道的值，方便看清每个颜色分量的大小
    print('拆包后：b（蓝） =', b)
    print('拆包后：g（绿） =', g)
    print('拆包后：r（红） =', r)

    # 7. 用 cvtColor() 把彩色图转成灰度图
    #    COLOR_BGR2GRAY：BGR 三通道压缩成一个亮度通道
    #    转换公式大致是：Gray = 0.114*B + 0.587*G + 0.299*R
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 8. 打印灰度图的 shape
    #    灰度图只有两个维度 (高, 宽)，没有通道数这一项
    #    例如由 (2094, 1486, 3) 变成 (2094, 1486)
    print('灰度图 shape（高, 宽）:', img_gray.shape)

    # 9. 读取灰度图同一位置 (1047, 743) 的像素值
    #    灰度图每个像素只有 1 个数（亮度值，0~255）
    #    对比：彩色图读出 3 个数（B、G、R），灰度图只读出 1 个数
    gray_value = img_gray[1047, 743]

    # 打印灰度图该位置的像素值
    print('灰度图 img_gray[1047, 743] 的像素值:', gray_value)

    # 10. 用切片截取一块 ROI（Region of Interest，感兴趣区域）
    #     切片写法 img[行的范围, 列的范围]
    #     img[100:200, 100:200] 表示：
    #       行（高方向）取第 100 行到第 199 行，共 200 - 100 = 100 行
    #       列（宽方向）取第 100 列到第 199 列，共 200 - 100 = 100 列
    #     注意切片是"含头不含尾"：包含起点 100，不包含终点 200
    roi = img[100:200, 100:200]

    # 打印 ROI 的 shape
    #    结果是 (100, 100, 3)：高 100、宽 100、3 个通道
    #    说明 ROI 是从原图上"切"下来的一个 100×100 的小方块
    print('ROI img[100:200, 100:200] 的 shape:', roi.shape)

    # 顺便把截取的 ROI 保存下来，方便查看效果
    cv2.imwrite('pic1_roi.jpg', roi)

    # =========================================================
    # 下面新增：修改像素值——改一个点、画一个色块
    # =========================================================

    # 1. 重新读取原图，并用 .copy() 复制一份再改
    #    直接改 img 会把原图数据也改掉（数组是引用传递），所以要 copy
    img2 = img.copy()

    # 2. 修改一个像素：把 (50, 50) 改成绿色
    #    BGR 顺序：[0, 255, 0] 表示蓝0、绿255、红0 → 纯绿色
    img2[50, 50] = [0, 255, 0]

    # 打印确认：一个点太小肉眼看不见，但数据确实变了
    print('修改后 img2[50, 50] =', img2[50, 50])

    # 3. 修改一片区域：把 行200~500、列200~500 的整块改成红色
    #    一行代码改 300×300 = 90000 个像素，这就是数组批量赋值的威力
    img2[200:500, 200:500] = [0, 0, 255]

    # 打印色块中心和色块外的点，对比验证
    print('红块中心 img2[350, 350] =', img2[350, 350], '← 已变成红色')
    print('红块外面 img2[50, 600] =', img2[50, 600], '← 白色，未受影响')

    # 4. 显示修改后的图片，肉眼确认
    #    看到鸭子图上多了一块红色方块（一个绿色点太小，肉眼几乎看不出来）
    cv2.imshow('modified', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 5. 保存修改后的图片
    cv2.imwrite('pic1_modified.jpg', img2)

    # =========================================================
    # 下面新增：通道拆分与合并
    # =========================================================

    # 1. 用 cv2.split() 把彩色图拆成 3 张单通道图
    #    返回值依次是蓝、绿、红三个二维数组（每个形状都是 高×宽）
    b, g, r = cv2.split(img)
    print('拆分后 b 的形状:', b.shape, '← 从三维变二维，只剩一个通道')

    # 打印同一个位置在三个通道里的值，和任务一的读数对上
    print('b[1047, 743] =', b[1047, 743], '，g =', g[1047, 743], '，r =', r[1047, 743])

    # 2. 只保留红色通道：把蓝、绿通道全部置 0
    #    这是一种很直观的"通道手术"——哪路通、哪路断，自己说了算
    #    手术后每个像素都变成 [0, 0, R]，画面会整体变成红色调
    img_red = img.copy()
    img_red[:, :, 0] = 0  # 所有行、所有列的第 0 通道（蓝）全部置 0
    img_red[:, :, 1] = 0  # 第 1 通道（绿）全部置 0
    print('只留红色通道后 img_red[1047, 743] =', img_red[1047, 743], '← 只剩 R=242')

    # 3. 用 cv2.merge() 把拆开的三个通道重新合并
    #    顺序必须还是 [b, g, r]，合出来的图和原图一模一样
    merged = cv2.merge([b, g, r])
    print('合并后与原图完全相同:', merged.shape == img.shape)

    # 4. 显示"只留红色通道"的效果图
    #    白背景（R=251）变成亮红，鸭子（R=200多）变成暗红，整体一片红
    cv2.imshow('red channel only', img_red)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # =========================================================
    # 下面新增：像素运算——图像融合
    # =========================================================

    # 1. 读入两张图，并统一缩放到 800×600
    #    ⚠️ cv2.add() 要求两张图尺寸、通道数完全相同，否则直接报错！
    #    pic1 是 2094×1486，pic5 是 720×1080，必须先 resize 成一样大
    imgA = cv2.resize(cv2.imread('pic1.jpg'), (800, 600))  # 鸭子（偏亮）
    imgB = cv2.resize(cv2.imread('pic5.jpg'), (800, 600))  # 母鸡（偏暗）
    print('imgA:', imgA.shape, ' imgB:', imgB.shape)

    # 2. 先看一个像素在相加前后的变化
    #    取 (300, 400) 这个点（行300、列400）
    print('imgA[300, 400] =', imgA[300, 400])
    print('imgB[300, 400] =', imgB[300, 400])

    # 3. 用 NumPy 的 + 号直接加（错误示范）
    #    uint8 溢出会"取模绕回"：400 % 256 = 144，亮处反而变暗
    print('imgA + imgB =', (imgA + imgB)[300, 400], '← R通道 236+164=400 取模绕回 144')

    # 4. 用 cv2.add() 相加（正确做法）
    #    超过 255 一律封顶在 255（饱和运算）
    img_add = cv2.add(imgA, imgB)
    print('cv2.add    =', img_add[300, 400], '← R通道 236+164=400 封顶 255')

    # 5. 显示相加结果：整体过亮发白（两张图的亮度叠加了）
    cv2.imshow('add result', img_add)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # =========================================================
    # 下面新增：加权融合（图像融合的标准做法）
    # =========================================================

    # 1. cv2.addWeighted(imgA, α, imgB, β, γ)
    #    公式：结果 = imgA×α + imgB×β + γ
    #    α=0.6、β=0.4：融合图里鸭子占六成、母鸡占四成；γ=0 不做亮度微调
    img_blend = cv2.addWeighted(imgA, 0.6, imgB, 0.4, 0)

    # 2. 打印同一个点验证公式
    #    0.6×102 + 0.4×32 + 0 = 74.0，OpenCV 四舍五入后就是 74
    print('img_blend[300, 400] =', img_blend[300, 400])
    print('验算: 0.6×102 + 0.4×32 + 0 = %.1f' % (0.6 * 102 + 0.4 * 32))

    # 3. 显示融合结果：两张图像"半透明"一样叠在一起
    cv2.imshow('blend result', img_blend)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 4. 保存融合图（作业要用）
    cv2.imwrite('blend_result.jpg', img_blend)
    print('融合图已保存为 blend_result.jpg')

    # =========================================================
    # 下面新增：阈值操作——图像二值化
    # =========================================================

    # 1. 读取 pic5（草地上的母鸡，明暗对比强），并转灰度图
    #    ⚠️ cv2.threshold() 只接受灰度图（单通道），彩图要先 cvtColor 转灰度
    img5 = cv2.imread('pic5.jpg')
    gray5 = cv2.cvtColor(img5, cv2.COLOR_BGR2GRAY)

    # 2. cv2.threshold(灰度图, 阈值, 最大值, 类型)
    #    含义：像素 > 127 → 变 255（白）；像素 ≤ 127 → 变 0（黑）
    #    返回两个值：
    #      ret  ：实际使用的阈值（固定阈值时就是传入的 127）
    #      binary：二值化后的黑白图
    ret5, binary5 = cv2.threshold(gray5, 127, 255, cv2.THRESH_BINARY)

    # 3. 打印阈值，确认 ret 的含义
    print('固定阈值 ret =', ret5)

    # 4. 分别显示灰度图和二值图，对比观察
    cv2.imshow('gray', gray5)
    cv2.imshow('binary 127', binary5)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 5. 保存二值图
    cv2.imwrite('binary_result.jpg', binary5)
    print('二值图已保存为 binary_result.jpg')

    # =========================================================
    # 下面新增：固定阈值的坑 + Otsu 自动阈值
    # =========================================================

    # 1. 读取 pic1（白背景的小黄鸭，整体很亮）并转灰度
    gray1 = cv2.cvtColor(cv2.imread('pic1.jpg'), cv2.COLOR_BGR2GRAY)

    # 2. 还是固定阈值 127
    #    pic1 的背景接近纯白（251），远大于 127 → 全部变白
    #    鸭子身体也比 127 亮 → 也变白：整张图几乎全白，鸭子"消失"了
    ret_a, bin_a = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)
    ratio_a = (bin_a == 255).sum() / bin_a.size * 100
    print('pic1 固定阈值127: 白色占比 %.1f%% ← 鸭子几乎消失' % ratio_a)

    # 3. 用 Otsu 算法自动找最佳阈值
    #    写法特点：阈值参数随手填 0（反正会被忽略），
    #    类型加上 cv2.THRESH_OTSU，OpenCV 会自动算出最合适的阈值
    #    返回的 ret_o 就是它自动算出来的阈值（pic1 算出的是 209）
    ret_o, bin_o = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ratio_o = (bin_o == 255).sum() / bin_o.size * 100
    print('pic1 Otsu: 自动阈值 =', ret_o, '，白色占比 %.1f%%' % ratio_o)

    # 4. 显示两种结果对比：左127几乎全白，右Otsu能看清鸭子轮廓
    cv2.imshow('fixed 127', bin_a)
    cv2.imshow('otsu', bin_o)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # =========================================================
    # 下面新增：权重实验——0.3/0.7、0.5/0.5、0.7/0.3 三组对比
    # =========================================================

    # 1. 三组权重各融合一张：α 是鸭子(imgA)的占比，β 是母鸡(imgB)的占比
    #    α+β=1，保证整体亮度不爆；α 越大画面越"像鸭子"，β 越大越"像母鸡"
    weights = [(0.3, 0.7), (0.5, 0.5), (0.7, 0.3)]
    blends = []
    for a, b in weights:
        blended = cv2.addWeighted(imgA, a, imgB, b, 0)
        blends.append(blended)
        out_name = 'blend_%.1f_%.1f.jpg' % (a, b)
        cv2.imwrite(out_name, blended)
        print('已保存 %s（鸭子 %.1f / 母鸡 %.1f）' % (out_name, a, b))

    # 2. 给每张图顶部写上权重标签，方便并排对比时一眼区分
    #    putText 不支持中文，所以标签用英文缩写 duck/hen
    labeled = []
    for (a, b), blended in zip(weights, blends):
        tag = blended.copy()
        cv2.rectangle(tag, (0, 0), (270, 40), (255, 255, 255), -1)  # 白底标签条
        cv2.putText(tag, 'duck %.1f / hen %.1f' % (a, b), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        labeled.append(tag)

    # 3. 用 np.hstack 把三张图横向拼成一张对比图（尺寸相同才能拼）
    compare = np.hstack(labeled)
    cv2.imwrite('blend_weights_compare.jpg', compare)
    print('三图对比已保存为 blend_weights_compare.jpg')

    cv2.imshow('blend weights compare', compare)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

