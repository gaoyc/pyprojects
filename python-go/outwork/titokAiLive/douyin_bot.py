"""
pip install flask requests cryptography qwen

Python 后端实现（接收弹幕 + 自动回复）

"""
from flask import Flask, request, jsonify
import hashlib
import time
import json
import requests
from qwen import Generation  # 通义千问 SDK
import os

app = Flask(__name__)

# 配置
TOKEN = "your_custom_token"  # 与抖音后台设置一致
CLIENT_KEY = "your_client_key"
CLIENT_SECRET = "your_client_secret"
QWEN_API_KEY = "your_qwen_api_key"

# 缓存 access_token
access_token_cache = {"token": None, "expires_at": 0}


def get_access_token():
    """获取抖音 API 访问令牌"""
    global access_token_cache
    if time.time() < access_token_cache["expires_at"]:
        return access_token_cache["token"]

    url = "https://open.douyin.com/oauth/access_token/"
    params = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credential"
    }
    resp = requests.get(url, params=params).json()
    token = resp["access_token"]
    expires_in = resp["expires_in"]
    access_token_cache.update({
        "token": token,
        "expires_at": time.time() + expires_in - 300  # 提前5分钟刷新
    })
    return token


def verify_douyin_request(signature, timestamp, nonce, echostr):
    """验证抖音 Webhook 请求合法性"""
    tmp = sorted([TOKEN, timestamp, nonce])
    tmp_str = "".join(tmp)
    hash_str = hashlib.sha1(tmp_str.encode()).hexdigest()
    return hash_str == signature


def generate_reply(comment_text):
    """根据弹幕生成回复（可结合预设规则 + AI）"""
    # 预设规则优先
    rules = {
        "价格": "点击下方购物车，今日特价¥399起！",
        "多少钱": "点击下方购物车，今日特价¥399起！",
        "宠物": "我们是宠物友好民宿，欢迎带毛孩子入住！",
        "早餐": "含双人自助早餐，7:00-10:00供应哦~",
        "取消": "支持免费取消，入住无忧！"
    }
    for keyword, reply in rules.items():
        if keyword in comment_text:
            return reply

    # 未匹配则调用 AI
    prompt = f"你是民宿客服，请用亲切简洁的话回答客人问题：{comment_text}"
    try:
        response = Generation.call(
            model="qwen-max",
            prompt=prompt,
            api_key=QWEN_API_KEY
        )
        return response.output.text[:100]  # 截断防超长
    except:
        return "感谢提问！请稍等管家为您解答~"


def send_customer_message(open_id, text):
    """向用户发送客服消息（需用户先发言）"""
    token = get_access_token()
    url = "https://open.douyin.com/im/msg/send/"
    headers = {"Content-Type": "application/json"}
    payload = {
        "touser_openid": open_id,
        "msgtype": "text",
        "text": {"content": text}
    }
    resp = requests.post(url, headers=headers, params={"access_token": token}, json=payload)
    print("Send message result:", resp.json())


@app.route("/douyin/webhook", methods=["GET", "POST"])
def webhook():
    # GET：抖音验证 URL 时调用
    if request.method == "GET":
        signature = request.args.get("signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = request.args.get("echostr")
        if verify_douyin_request(signature, timestamp, nonce, echostr):
            return echostr
        else:
            return "Invalid signature", 403

    # POST：接收事件（如弹幕）
    data = request.json
    print("Received event:", data)

    # 处理直播间评论事件
    if data.get("event") == "live_room_comment":
        event_data = data["data"]
        comment = event_data["comment"]
        user_open_id = event_data["user_open_id"]  # 用户唯一ID
        comment_text = comment["text"]

        # 生成回复
        reply = generate_reply(comment_text)
        print(f"User: {comment_text} → Reply: {reply}")

        # 发送客服消息（私信回复）
        send_customer_message(user_open_id, reply)

    return "success"


if __name__ == "__main__":
    app.run(port=5000)