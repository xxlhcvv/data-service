# -*- coding: utf-8 -*-
"""豆瓣读书 Top250 -- 最简单的 requests 请求示例"""

# 导入 requests 库，用来发送 HTTP 请求（没装的话先执行：pip install requests）
import requests
# 导入 BeautifulSoup，用来解析网页 HTML（没装的话先执行：pip install beautifulsoup4）
from bs4 import BeautifulSoup

# 目标网址：每页 25 本，start 表示从第几本书开始取（0=第 1~25 本，25=第 26~50 本）
# 本次把 start 改成 25，也就是爬取第二页的数据
url = "https://book.douban.com/top250?start=25"

# 请求头：把程序伪装成浏览器，否则豆瓣很可能拒绝访问（返回 418/403）
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# 发送 GET 请求；timeout=10 表示最多等待 10 秒，避免程序一直卡住
response = requests.get(url, headers=headers, timeout=10)

# 打印响应状态码：200 表示请求成功
print("响应状态码：", response.status_code)

# 手动指定编码为 utf-8，防止网页中文显示成乱码
response.encoding = "utf-8"

# 打印网页源代码的前 500 个字符（text 是字符串，可以用切片取前 500 个）
print("网页源代码前 500 个字符：")
print(response.text[:500])

# 用 BeautifulSoup 把网页源代码转成可以按标签查找的对象
# "html.parser" 是 Python 自带的解析器，不需要额外安装
soup = BeautifulSoup(response.text, "html.parser")

# soup.title 表示 <title> 标签，.string 取出标签里的文字，也就是网页标题
print("网页标题：", soup.title.string)

# ---------- 以下是新增部分：用 CSS 选择器抓取本页的图书列表 ----------

# select() 里写的就是 CSS 选择器：tr 表示标签名，.item 表示 class="item"
# 返回的是一个列表，列表里每个元素都是代表一行图书的 tr 标签
items = soup.select("tr.item")

# len() 用来数出列表里有多少个元素，也就是本页抓到了多少本书
print(f"本页共抓到图书：{len(items)} 本")

# for 循环把列表里的元素一个个取出来，item 就是当前这本书所在的 tr 标签
for item in items:
    # 在每一行里找“带 title 属性的 a 标签”：
    # 书名和链接都挂在这个 a 上，而封面图片那个 a 标签没有 title
    a = item.select_one("a[title]")

    # 万一某一行结构不同、找不到这样的 a，就跳过它，避免程序报错中断
    if a is None:
        continue

    # a.get("title") 取出 title 属性的值（书名），a.get("href") 取出 href（链接）
    # f"..." 是格式化字符串，会把 {} 里的变量替换成真正的值再打印
    print(f"{a.get('title')} | {a.get('href')}")
