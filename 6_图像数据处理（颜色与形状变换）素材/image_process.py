# -*- coding: utf-8 -*-
"""
OpenCV 图像读取入门：读取 pic1.jpg 并显示
未安装 OpenCV 可执行：pip install opencv-python
"""

# 导入 OpenCV 库
import cv2
import numpy as np

# 导入 sys 模块，用于修改终端输出编码
import sys

# Windows 命令行默认 GBK 编码，输出特殊字符时可能报错，改成 utf-8 更稳妥
sys.stdout.reconfigure(encoding='utf-8')

# 图片文件名（相对路径，表示在本 .py 文件所在的目录下找 pic1.jpg）
file_name = 'pic1.jpg'

# 1. 用 imread() 读取图片
#    读取成功时返回一个 NumPy 数组（三维：高×宽×通道数）
#    读取失败时返回 None，不会报错，所以必须自己判断
img = cv2.imread(file_name)

# 2. 判断图片是否读取成功
if img is None:
    # 读取失败时打印两种最常见的原因
    print('图片读取失败！常见原因：')
    print('1. 文件不在本 .py 文件的同一目录下（当前找不到', file_name, '）')
    print('2. 文件路径中含有中文，cv2.imread() 对中文路径支持不好')
    print('   解决办法：把图片移到英文路径下，或用 np.fromfile() + cv2.imdecode() 读取')
else:
    # 读取成功，打印图片的基本信息
    print('图片读取成功')

    # shape 是图像的形状，返回 (高, 宽, 通道数)
    # 例如 (480, 640, 3) 表示：高 480 像素、宽 640 像素、3 个颜色通道（BGR）
    print('shape（高, 宽, 通道数）:', img.shape)

    # dtype 是数组中每个元素的数据类型
    # 图像通常是 uint8，即 0~255 的无符号整数
    print('dtype:', img.dtype)

    # 取左上角 (0, 0) 位置的像素值
    # 写法是 img[行, 列]，行=高方向、列=宽方向，注意不是 (x, y)
    # OpenCV 读取的颜色顺序是 BGR，所以这里返回 [蓝, 绿, 红]
    print('左上角 (0,0) 的像素值（BGR）:', img[0, 0])

    # 3. 用 imshow() 弹出窗口显示图片
    #    参数1 是窗口标题，参数2 是要显示的图像数据
    cv2.imshow('pic1', img)

    # 4. 用 waitKey(0) 等待按键
    #    参数 0 表示无限等待，直到用户按下任意键
    #    这一句必须写，否则窗口会一闪而过
    cv2.waitKey(0)

    # 5. 用 destroyAllWindows() 关闭所有弹出的窗口，释放资源
    cv2.destroyAllWindows()
    # =========================================================
    # 下面新增：颜色空间转换 + 拼接对比显示
    # =========================================================

    # 1. 重新读取原图（imread 读进来的是 BGR 格式），并判断是否成功
    img2 = cv2.imread(file_name)

    if img2 is None:
        # 读取失败时给出提示（常见原因同上：文件不在同目录、路径含中文）
        print('图片读取失败：找不到 pic1.jpg，或路径中含有中文')
    else:
        # 2. 用 cvtColor() 做颜色空间转换
        #    语法：cv2.cvtColor(输入图像, 转换标志)
        #    转换标志的命名规律是「COLOR_源空间2目标空间」

        # BGR -> RGB：把 OpenCV 默认的蓝绿红顺序改成常见的红绿蓝
        img_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
        # 保存 RGB 图
        cv2.imwrite('pic1_rgb.jpg', img_rgb)

        # BGR -> GRAY：转灰度图，三个通道压缩成一个亮度通道
        img_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # 保存灰度图
        cv2.imwrite('pic1_gray.jpg', img_gray)

        # BGR -> HSV：色调(H)、饱和度(S)、明度(V)，常用于按颜色分割目标
        img_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        # 保存 HSV 图
        cv2.imwrite('pic1_hsv.jpg', img_hsv)

        # BGR -> YCrCb：亮度(Y) + 红色差(Cr) + 蓝色差(Cb)，常用于肤色检测和图像压缩
        img_ycrcb = cv2.cvtColor(img2, cv2.COLOR_BGR2YCrCb)
        # 保存 YCrCb 图
        cv2.imwrite('pic1_ycrcb.jpg', img_ycrcb)

        # 3. 打印原图和四种转换结果的 shape
        print('原图 BGR  的 shape:', img2.shape)
        print('RGB      的 shape:', img_rgb.shape)
        print('GRAY     的 shape:', img_gray.shape)
        print('HSV      的 shape:', img_hsv.shape)
        print('YCrCb    的 shape:', img_ycrcb.shape)

        # 4. 把原图和灰度图横向拼接成对比图
        #    拼接要求两张图的通道数相同，
        #    原图是 3 通道、灰度图是 1 通道，所以先把灰度图补回 3 通道
        #    GRAY2BGR 会把这个亮度值复制三份，看起来仍是灰色
        img_gray_3c = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

        # hconcat() 表示横向拼接（水平方向并排）；想要上下拼接可用 vconcat()
        combine = cv2.hconcat([img2, img_gray_3c])

        # 把拼接图缩小到原来的一半，避免图片太大超出屏幕
        # dsize=(0, 0) 配合 fx、fy 使用，fx/fy 是宽和高的缩放比例
        combine_small = cv2.resize(combine, (0, 0), fx=0.5, fy=0.5)

        # 弹出窗口显示对比图（左边原图，右边灰度图）
        cv2.imshow('BGR vs GRAY', combine_small)

        # 等待按键，0 表示一直等到用户按下任意键
        cv2.waitKey(0)

        # 关闭所有窗口，释放资源
        cv2.destroyAllWindows()

# =========================================================
# 下面新增：图像缩放变换
# =========================================================

# 1. 读取原图，并判断是否成功
image = cv2.imread(file_name)

if image is None:
    # 读取失败时的提示（原因同上：文件不在同目录、或路径含中文）
    print('图片读取失败：找不到 pic1.jpg，或路径中含有中文')
else:
    # 2. 打印原图的高和宽
    #    image.shape 的前两位是 (高, 宽)，第三位才是通道数
    #    shape[0] 是高（行数），shape[1] 是宽（列数）
    height = image.shape[0]
    width = image.shape[1]
    print('原图的高:', height)
    print('原图的宽:', width)
    print('原图 shape（高, 宽, 通道数）:', image.shape)

    # 3. 缩放到固定尺寸 400×300
    #    resize() 的第二个参数 dsize 是 (宽, 高)，注意顺序和 shape 相反！
    #    这里 (400, 300) 表示：宽 400、高 300
    resize_fixed = cv2.resize(image, (400, 300))

    # 保存固定尺寸缩放后的图片
    cv2.imwrite('pic1_resize_fixed.jpg', resize_fixed)

    # 打印固定尺寸缩放后的 shape
    print('固定尺寸 400×300 后的 shape:', resize_fixed.shape)

    # 4. 按比例缩放：宽和高都变成原来的 0.5 倍
    #    dsize 写 None（或 (0, 0)），表示"目标尺寸由 fx、fy 决定"
    #    fx 是宽方向的缩放倍数，fy 是高方向的缩放倍数
    resize_scale = cv2.resize(image, None, fx=0.5, fy=0.5)

    # 保存按比例缩放后的图片
    cv2.imwrite('pic1_resize_scale.jpg', resize_scale)

    # 打印按比例缩放后的 shape
    print('按 0.5 倍缩放后的 shape:', resize_scale.shape)

    # 顺带算一下：验证 shape 的前两位确实是原图的一半
    print('原图高的一半:', height * 0.5, '，缩放后高:', resize_scale.shape[0])
    print('原图宽的一半:', width * 0.5, '，缩放后宽:', resize_scale.shape[1])
# =========================================================
# 下面新增：图像平移变换（向右 100 像素、向下 50 像素）
# =========================================================

# 1. 读取原图，并判断是否成功
img3 = cv2.imread(file_name)

if img3 is None:
    # 读取失败时给出提示（常见原因：文件不在同目录、或路径含中文）
    print('图片读取失败：找不到 pic1.jpg，或路径中含有中文')
else:
    # 2. 取出原图的高和宽
    #    shape[0] 是高（行方向，也就是 y 方向）
    #    shape[1] 是宽（列方向，也就是 x 方向）
    h = img3.shape[0]
    w = img3.shape[1]

    # 3. 用 numpy 构造 2×3 的平移矩阵（仿射变换矩阵的前两行）
    #
    #    矩阵写成两行：
    #        [[1, 0, 100],
    #         [0, 1,  50]]
    #
    #    矩阵里每个数字的含义：
    #      第 1 行第 1 个数 1   ：x 方向的缩放倍数，1 表示横向不缩放
    #      第 1 行第 2 个数 0   ：x 方向的错切/旋转分量，0 表示不倾斜
    #      第 1 行第 3 个数 100 ：x 方向（水平）平移的像素数，正数是向右移，负数是向左移
    #      第 2 行第 1 个数 0   ：y 方向的错切/旋转分量，0 表示不倾斜
    #      第 2 行第 2 个数 1   ：y 方向的缩放倍数，1 表示纵向不缩放
    #      第 2 行第 3 个数 50  ：y 方向（垂直）平移的像素数，正数是向下移，负数是向上移
    #
    #    一句话记法：[[a, b, tx],
    #                 [c, d, ty]]
    #    其中 a、d 控制缩放，b、c 控制旋转/倾斜，最后一列 tx、ty 就是 x、y 方向的移动像素数
    #
    #    dtype=np.float32 是 OpenCV 的要求：warpAffine 的变换矩阵必须是 32 位浮点类型
    #    （int 类型会报错：OpenCV(4.x) ... src data type is not supported）
    M = np.array([[1, 0, 100],
                  [0, 1, 50]], dtype=np.float32)

    # 打印矩阵，确认里面的数字
    print('平移矩阵 M：')
    print(M)

    # 4. 用 warpAffine() 执行仿射变换（这里就是平移）
    #    参数1 src    ：输入图像
    #    参数2 M      ：2×3 的变换矩阵（上面构造的）
    #    参数3 dsize  ：输出图像的尺寸，格式是 (宽, 高)，这里写成 (w, h) 表示与原图尺寸相同
    #                   注意顺序是 (宽, 高)，和 shape 的 (高, 宽, 通道) 相反
    img_translate = cv2.warpAffine(img3, M, (w, h))

    # 5. 保存平移后的图片
    cv2.imwrite('pic1_translate.jpg', img_translate)

    # 打印原图和平移后图片的 shape，验证尺寸完全一致
    print('原图 shape（高, 宽, 通道数）:', img3.shape)
    print('平移后 shape（高, 宽, 通道数）:', img_translate.shape)

    # 6. 显示平移后的图片
    cv2.imshow('translate', img_translate)

    # 等待按键，0 表示一直等到用户按下任意键
    cv2.waitKey(0)

    # 关闭所有窗口，释放资源
    cv2.destroyAllWindows()# =========================================================
# 下面新增：图像旋转（绕图像中心逆时针旋转 45 度）
# =========================================================

# 1. 读取原图，并判断是否成功
img4 = cv2.imread(file_name)

if img4 is None:
    # 读取失败时给出提示（常见原因：文件不在同目录、或路径含中文）
    print('图片读取失败：找不到 pic1.jpg，或路径中含有中文')
else:
    # 2. 取出原图的高和宽
    #    shape[0] 是高（y 方向），shape[1] 是宽（x 方向）
    h4 = img4.shape[0]
    w4 = img4.shape[1]

    # 3. 计算图像中心的坐标
    #    中心点 = (宽 / 2, 高 / 2)，注意是 (x, y) 也就是 (列, 行) 的顺序
    #    // 是整除，得到整数像素坐标（OpenCV 要求坐标是整数）
    center = (w4 // 2, h4 // 2)
    print('图像中心坐标 (x, y):', center)

    # 4. 用 cv2.getRotationMatrix2D() 生成旋转矩阵
    #    参数1 center：旋转中心，这里填图像中心，表示绕中心旋转
    #    参数2 angle ：旋转角度，正数表示逆时针，负数表示顺时针
    #                   这里填 45，就是逆时针 45 度
    #    参数3 scale ：缩放倍数，1.0 表示只旋转、不改变大小
    #    返回值是一个 2×3 的 numpy 数组，类型已经是 float64（OpenCV 可直接用）
    M_rotate = cv2.getRotationMatrix2D(center, 45, 1.0)

    # 5. 打印旋转矩阵，观察它的结构
    print('旋转矩阵 M_rotate：')
    print(M_rotate)

    # 6. 用 warpAffine() 执行旋转变换
    #    参数3 dsize 是 (宽, 高)，这里保持原图尺寸
    #    旋转后超出原图范围的角会被裁掉，空出来的区域默认填充黑色
    img_rotate = cv2.warpAffine(img4, M_rotate, (w4, h4))

    # 7. 保存旋转后的图片
    cv2.imwrite('pic1_rotate.jpg', img_rotate)

    # 打印原图和旋转后图片的 shape，确认尺寸相同
    print('原图 shape（高, 宽, 通道数）:', img4.shape)
    print('旋转后 shape（高, 宽, 通道数）:', img_rotate.shape)

    # 8. 显示旋转后的图片
    cv2.imshow('rotate', img_rotate)

    # 等待按键，0 表示一直等到用户按下任意键
    cv2.waitKey(0)

    # 关闭所有窗口，释放资源
    cv2.destroyAllWindows()
# =========================================================
# 下面新增：图像翻转变换（水平、垂直、水平+垂直）
# =========================================================

# 1. 读取原图，并判断是否成功
img5 = cv2.imread(file_name)

if img5 is None:
    # 读取失败时给出提示（常见原因：文件不在同目录、或路径含中文）
    print('图片读取失败：找不到 pic1.jpg，或路径中含有中文')
else:
    # 2. 用 cv2.flip() 做翻转变换
    #    语法：cv2.flip(输入图像, flipCode)
    #    第二个参数 flipCode（翻转方向）的含义：
    #      1  ：水平翻转（左右镜像），沿垂直中轴线翻，等于照镜子
    #           第 1 列和第 n 列互换，第 2 列和第 n-1 列互换……
    #      0  ：垂直翻转（上下颠倒），沿水平中轴线翻
    #           第 1 行和第 m 行互换，第 2 行和第 m-1 行互换……
    #      -1 ：水平 + 垂直同时翻转（等价于把图旋转 180 度）
    #           先左右翻再上下翻，行和列都倒过来

    # 水平翻转：flipCode = 1，左右镜像
    flip_h = cv2.flip(img5, 1)

    # 垂直翻转：flipCode = 0，上下颠倒
    flip_v = cv2.flip(img5, 0)

    # 水平 + 垂直翻转：flipCode = -1，两个方向同时翻
    flip_both = cv2.flip(img5, -1)

    # 3. 分别保存三张翻转后的图片
    cv2.imwrite('pic1_flip_h.jpg', flip_h)
    cv2.imwrite('pic1_flip_v.jpg', flip_v)
    cv2.imwrite('pic1_flip_both.jpg', flip_both)

    # 4. 打印翻转前后的 shape
    print('原图 shape（高, 宽, 通道数）        :', img5.shape)
    print('水平翻转后 shape（高, 宽, 通道数）  :', flip_h.shape)
    print('垂直翻转后 shape（高, 宽, 通道数）  :', flip_v.shape)
    print('水平+垂直翻转后 shape（高, 宽, 通道数）:', flip_both.shape)

    # 说明：翻转只是把已有像素的位置重新排列（行或列的顺序倒过来），
    #       既不增删像素，也不做插值计算，
    #       所以高、宽、通道数完全不变，shape 与翻转前一致

    # 5. 把原图和三种翻转结果缩小后横向拼接，方便对比观察
    #    先把四张图统一缩到同样的高度，避免尺寸不一致无法拼接
    #    这里统一缩放到固定尺寸 400×300（注意 dsize 是 (宽, 高)）
    show_list = [img5, flip_h, flip_v, flip_both]
    show_small = [cv2.resize(x, (400, 300)) for x in show_list]

    # hconcat() 横向拼接四张小图：原图 | 水平 | 垂直 | 双向
    combine_flip = cv2.hconcat(show_small)

    # 弹出窗口显示对比图
    cv2.imshow('flip: original | H | V | BOTH', combine_flip)

    # 等待按键，0 表示一直等到用户按下任意键
    cv2.waitKey(0)

    # 关闭所有窗口，释放资源
    cv2.destroyAllWindows()
# -*- coding: utf-8 -*-
"""
批量处理当前目录下的 pic1.jpg ~ pic5.jpg：
读取 -> 转灰度 -> 缩放到 200×200 -> 另存为新文件
需要库：opencv-python
未安装可执行：pip install opencv-python
"""

# 导入 OpenCV 库，用于读取、灰度转换、缩放、保存图片
import cv2

# 导入 sys 模块，用于修改终端输出编码
import sys

# Windows 命令行默认 GBK 编码，打印特殊字符时可能报错，改成 utf-8 更稳妥
sys.stdout.reconfigure(encoding='utf-8')

# 1. 用 for 循环遍历 1 到 5
#    range(1, 6) 生成 1、2、3、4、5（注意结束值 6 取不到，这是 Python 的规则）
for i in range(1, 6):

    # 2. 用 f-string 拼出文件名
    #    f'pic{i}.jpg' 里的 {i} 会被替换成当前的数字
    #    例如 i=1 时得到 'pic1.jpg'，i=2 时得到 'pic2.jpg'
    input_name = f'pic{i}.jpg'

    # 用 f-string 拼出要保存的新文件名
    #    例如 i=1 时得到 'pic1_gray_200.jpg'
    output_name = f'pic{i}_gray_200.jpg'

    # 3. 读取这张图片
    #    imread() 成功返回 numpy 数组，失败返回 None（不会报错，所以要自己判断）
    img = cv2.imread(input_name)

    # 4. 判断图片是否读取成功
    if img is None:
        # 读取失败：打印提示信息
        print(f'第 {i} 张：{input_name} 读取失败，已跳过（文件不存在或路径含中文）')

        # continue 表示立即结束本轮循环，直接进入下一次循环（i 变成下一个数）
        # 这样即使某张图缺失，程序也不会中断，会继续处理后面的图片
        continue

    # 5. 转成灰度图
    #    cvtColor(输入图像, 转换标志)：COLOR_BGR2GRAY 表示 BGR 彩图转灰度图
    #    转换后通道数从 3 变成 1，shape 由 (高, 宽, 3) 变成 (高, 宽)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 6. 统一缩放到 200×200
    #    resize() 的第二个参数 dsize 是 (宽, 高)，顺序和 shape 的 (高, 宽) 相反
    #    这里 (200, 200) 表示宽 200、高 200，无论原图多大都会被拉伸成这个尺寸
    img_resize = cv2.resize(img_gray, (200, 200))

    # 7. 另存为新文件
    #    imwrite() 保存成功返回 True，失败返回 False
    save_ok = cv2.imwrite(output_name, img_resize)

    # 8. 每处理一张就打印一条记录
    #    包含：原文件名、原始 shape、处理后的 shape
    print(f'第 {i} 张：原文件 {input_name} | 原始 shape {img.shape} '
          f'| 处理后 shape {img_resize.shape} | 已保存为 {output_name}：{save_ok}')

# 9. 全部循环结束后打印完成提示
print('批量处理结束：pic1.jpg ~ pic5.jpg 已全部处理完毕')