# -*- coding: utf-8 -*-
"""深圳 Q 房网：提取指定页面中“在售房源”的链接"""

# 导入 csv，用来把爬取结果保存成表格文件
import csv
# 导入 re，用来做正则匹配（提取价格里的数字）
import re
# 导入 sys，用来设置控制台输出编码
import sys
# 导入 time，用来在重试之间等待几秒
import time
# 导入 requests 库，用来发送 HTTP 请求（没装的话先执行：pip install requests）
import requests
# 导入 BeautifulSoup，用来解析网页 HTML（没装的话先执行：pip install beautifulsoup4）
from bs4 import BeautifulSoup

# 主域名：过滤出来的相对链接要拼上它，才能变成可以访问的完整链接
BASE_URL = "https://shenzhen.qfang.com"

# 请求头：定义在最外层成为全局变量，get_links 和 get_info 两个函数都能复用
# 作用是把程序伪装成 Chrome 浏览器，否则网站可能拒绝访问（返回 403 等）
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def get_links(url):
    """请求 url，提取 div.list-main-header.clearfix 下所有以 /sale/ 开头的 a 标签链接。

    参数:
        url: 要爬取的网页地址
    返回:
        拼好主域名、去掉问号参数的完整链接列表
    """
    # 请求头直接复用上面定义好的全局 headers，这里不用再重复定义

    # 发送 GET 请求；timeout=10 表示最多等待 10 秒，避免程序一直卡住
    # 网络偶发超时、502 等故障很常见，所以最多自动重试 3 次
    for attempt in range(1, 4):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            break  # 请求成功就跳出重试循环
        except requests.RequestException as e:
            # 打印第几次失败、失败原因；常见原因：代理不稳定、断网、网站临时故障
            print(f"第 {attempt} 次请求失败：{e}")
            if attempt == 3:
                # 3 次都失败，放弃并返回空列表
                return []
            time.sleep(2)  # 等 2 秒再重试，给网络/网站一点恢复时间

    # 状态码不是 200 时提示（比如 502 表示网站服务端出故障，只能等它恢复）
    if response.status_code != 200:
        print(f"网站返回异常状态码：{response.status_code}")
        return []

    # 手动指定编码为 utf-8，防止网页中文显示成乱码
    response.encoding = "utf-8"

    # 用 BeautifulSoup 把网页源代码转成可以按标签查找的对象
    # "html.parser" 是 Python 自带的解析器，不需要额外安装
    soup = BeautifulSoup(response.text, "html.parser")

    # select() 里写的就是 CSS 选择器：
    # div.list-main-header.clearfix 表示同时带这两个 class 的 div，> a 表示它的直接子标签 a
    # 返回的是一个列表，列表里每个元素都是代表一个 a 标签的对象
    a_tags = soup.select("div.list-main-header.clearfix > a")

    # 准备一个空列表，用来装最后要返回的完整链接
    links = []

    # for 循环把列表里的元素一个个取出来，a 就是当前这个 a 标签
    for a in a_tags:
        # 取出 href 属性；有些 a 标签可能没有 href，这时拿到的是 None
        href = a.get("href")

        # 没有 href 的标签直接跳过，避免后面报错
        if href is None:
            continue

        # 只要以 /sale/ 开头的链接（其他如 /rent/ 租房等通通不要）
        if not href.startswith("/sale/"):
            continue

        # split("?")[0] 表示以问号切开后取第一部分，也就是去掉问号后面的参数（如 ?page=2）
        href = href.split("?")[0]

        # 相对链接拼上主域名，组成可以正常访问的完整链接，然后加入结果列表
        full_url = BASE_URL + href
        links.append(full_url)

    # 把收集好的完整链接列表返回给调用者
    return links


def get_info(url):
    """请求房源详情页 url，提取标题、总价、户型、建筑面积。

    参数:
        url: 房源详情页地址
    返回:
        字典，包含 标题 / 总价 / 户型 / 建筑面积 / 链接
    """
    # 复用全局的 headers 发送 GET 请求；timeout=10 表示最多等 10 秒
    # 网络偶发超时、502 等故障很常见，所以最多自动重试 3 次
    # response 先设为 None，只有拿到正常响应（状态码 200）才会被赋值
    response = None
    for attempt in range(1, 4):
        try:
            r = requests.get(url, headers=headers, timeout=10)
            # 只有状态码 200 才算是真正的成功，其他情况（如 502）继续重试
            if r.status_code == 200:
                response = r
                break  # 成功就跳出重试循环
        except requests.RequestException:
            # 网络异常（超时、连接中断等）不打印任何内容，直接进入下一次重试
            pass

        # 前两次失败后等 2 秒再重试，给网络和网站一点恢复时间
        if attempt < 3:
            time.sleep(2)

    # 3 次都没拿到正常响应，返回空字典（本函数严禁 print）
    if response is None:
        return {}

    # 手动指定编码为 utf-8，防止网页中文显示成乱码
    response.encoding = "utf-8"

    # 用 Python 自带的 html.parser 把网页源代码转成可以按标签查找的对象
    soup = BeautifulSoup(response.text, "html.parser")

    # ---------- 1. 房源标题：h2.house-title ----------
    # select_one() 只取第一个匹配的元素，找不到时返回 None
    title_tag = soup.select_one("h2.house-title")
    # 三元表达式：找到就取标签里的文字，找不到就给空字符串，避免 None 报错
    title = title_tag.get_text(strip=True) if title_tag else ""

    # ---------- 2. 总价：div.price-wrap ----------
    total_price = ""  # 先准备空字符串，匹配到再覆盖
    price_tag = soup.select_one("div.price-wrap")
    if price_tag:
        # get_text(" ", strip=True) 把标签内的文字拼成一整串，形如："197 万 29994元/㎡ ..."
        price_text = price_tag.get_text(" ", strip=True)
        # 正则：\d+(?:\.\d+)? 匹配整数或小数，\s*万 表示数字后可以隔空格再跟一个“万”字
        match = re.search(r"(\d+(?:\.\d+)?)\s*万", price_text)
        if match:
            # group(1) 取出括号里捕获的数字部分，即 "197"
            total_price = match.group(1)

    # ---------- 3. 户型 和 建筑面积：div.house-info clearfix 下的 li ----------
    house_type = ""  # 房屋户型
    house_area = ""  # 建筑面积

    # select() 会取出页面上所有符合条件的 li（“基本属性”“交易属性”两块都在里面）
    for li in soup.select("div.house-info.clearfix li"):
        # 每个 li 的文字里同时包含名称和值，例如 "房屋户型 2 室2厅1厨1卫"
        li_text = li.get_text(" ", strip=True)

        # 值放在子标签 div.text 里，取不到就跳过这一条
        text_tag = li.select_one("div.text")
        if text_tag is None:
            continue

        # 用正则把换行、多余空格全部去掉，"2 室2厅1厨1卫" 就变成 "2室2厅1厨1卫"
        value = re.sub(r"\s+", "", text_tag.get_text())

        # 判断 li 的文字里含哪个关键词，就把值存进对应的变量
        if "房屋户型" in li_text:
            house_type = value
        elif "建筑面积" in li_text:
            house_area = value

    # 把 4 个字段和详情页链接一起放进字典返回
    return {
        "标题": title,
        "总价": total_price,
        "户型": house_type,
        "建筑面积": house_area,
        "链接": url,
    }


# 只有直接运行本文件时才会执行下面的测试代码（被 import 时不会执行）
if __name__ == "__main__":
    # Windows 控制台默认是 GBK 编码，打印 “㎡” 这类字符会报 UnicodeEncodeError
    # 统一改成 utf-8 输出，errors="replace" 表示编不出来的字符用 ? 代替，保证不中断
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # 房源序号，从 1 开始，每成功写入一条数据就加 1
    number = 1
    # 记录总共成功保存了多少条房源
    count = 0

    # 打开 csv 文件保存结果
    # encoding="utf-8-sig" 会在文件开头写 BOM，Excel 打开中文不乱码
    # newline="" 是为了避免 Windows 下每行之间多出空行
    # with 管理文件：整个爬取过程保持打开，每抓到一条就立刻写入，中途出错也不会丢数据
    with open("qfang_fangyuan.csv", "w", newline="", encoding="utf-8-sig") as f:
        # 创建 csv 写入对象
        writer = csv.writer(f)

        # 先写表头（本次新增了【页码】字段）
        writer.writerow(["序号", "页码", "标题", "总价", "户型", "建筑面积", "链接"])

        # 循环爬取第 1 页到第 5 页（range(1, 6) 产生的值是 1~5）
        # 列表页地址形如：https://shenzhen.qfang.com/sale/f1 ... /sale/f5
        # 注意：Q 房网的分页是 /sale/f页码，写成 /sale/页码 会跳到 404 页面取不到数据
        for page in range(1, 6):
            # 拼接第 page 页的列表页地址
            list_url = f"{BASE_URL}/sale/f{page}"
            print(f"正在爬取第 {page} 页：{list_url}")

            # 调用已有的 get_links 函数，拿到这一页的所有房源详情页链接
            links = get_links(list_url)
            print(f"第 {page} 页共获取到 {len(links)} 条房源链接")

            # 遍历这一页的每条链接，逐条进入详情页抓信息
            for link in links:
                # 调用已有的 get_info 函数，接收返回的字典
                info = get_info(link)

                # 空字典说明这条抓取失败，跳过它；延时不省，直接处理下一条
                if not info:
                    time.sleep(2)
                    continue

                # 打印 序号、页码、标题、总价、建筑面积
                print(
                    f"{number}. 第 {page} 页 | {info['标题']} | "
                    f"总价：{info['总价']} 万 | 建筑面积：{info['建筑面积']}"
                )

                # 写入 csv 这一条数据，第 2 列记录它所属的页码 page
                writer.writerow(
                    [
                        number,
                        page,
                        info["标题"],
                        info["总价"],
                        info["户型"],
                        info["建筑面积"],
                        info["链接"],
                    ]
                )

                # 序号和计数都加 1
                number += 1
                count += 1

                # 单条爬取完成，暂停 2 秒，避免请求太快被网站限流或封 IP
                time.sleep(2)

            # 每页抓取完成，暂停 3 秒再进行下一页
            time.sleep(3)

    # 全部爬取结束后的完成提示
    print(f"爬取完成！共保存 {count} 条房源信息到 qfang_fangyuan.csv")
