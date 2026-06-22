import requests


def send_serverchan_message(sckey, title, content):
    """
    向 Server酱 发送消息
    :param sckey: 你的 Server酱 SendKey
    :param title: 消息标题（必填）
    :param content: 消息内容（支持Markdown，可选）
    """
    # 这是官方的API地址[reference:12][reference:13]
    url = f"https://sctapi.ftqq.com/{sckey}.send"

    # 构造要发送的数据
    data = {
        "title": title,
        "desp": content  # 内容支持Markdown格式[reference:14][reference:15]
    }

    try:
        response = requests.post(url, data=data)
        result = response.json()

        if result.get('code') == 0:
            print("✅ 消息发送成功！")
        else:
            print(f"❌ 消息发送失败: {result.get('message')}")

    except requests.RequestException as e:
        print(f"❌ 请求出错: {e}")
