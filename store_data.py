# -*- coding: utf-8 -*-
"""端侧采集练习：用 OpenCV 连拍 10 张照片（无摄像头时自动改用本地视频代替）"""

# 导入 OpenCV（没装的话先执行：pip install opencv-python）
import cv2

# ---------- 第一步：打开视频源 ----------
# 先尝试打开默认摄像头（编号 0 对应本机第一个摄像头，通常就是笔记本自带的那颗）
cap = cv2.VideoCapture(0)

# 如果没有摄像头、或被其他程序占用，cap.isOpened() 会返回 False
# 这种情况下改用本地视频文件代替，端侧采集练习依然能跑通
if not cap.isOpened():
    print("默认摄像头不可用，改用本地视频文件 TomAndJerry.mp4 代替")
    cap.release()  # 先把刚才空对象释放掉，避免资源泄露
    cap = cv2.VideoCapture("TomAndJerry.mp4")
    # 视频文件也打不开就直接退出，避免后面空指针报错
    if not cap.isOpened():
        print("视频文件 TomAndJerry.mp4 也无法打开，请确认它是否在脚本同目录")
        cap.release()
        exit()

# ---------- 第二步：用 for 循环连拍 10 张照片 ----------
# range(1, 11) 产生的值是 1、2、3 ... 10，正好对应 10 张照片
for i in range(1, 11):
    # cap.read() 读取一帧画面
    # ret：布尔值，这一帧是否读取成功
    # frame：画面本身（numpy 数组）
    # 视频文件读到末尾时 ret 会变 False；摄像头取流一般不会
    ret, frame = cap.read()

    if not ret:
        print(f"第 {i} 张读取失败（可能视频已到末尾），提前结束")
        break

    # 用 f-string 拼文件名：photo_1.jpg ... photo_10.jpg
    filename = f"photo_{i}.jpg"

    # imwrite() 把当前帧写入磁盘，返回值表示是否成功
    saved = cv2.imwrite(filename, frame)
    if saved:
        print(f"第 {i} 张已保存：{filename}")
    else:
        print(f"第 {i} 张保存失败（请检查当前目录是否有写入权限）")

# ---------- 第三步：无论拍了多少张，都统一释放资源 ----------
# 否则摄像头 / 视频解码器会一直被本次进程占用
cap.release()
print("采集完成，已释放摄像头/视频资源")