"""
对接民宿 PMS 系统动态生成价格语音
假设你的 PMS（Property Management System）提供 API，返回今日房价。

场景示例
PMS 返回：{"room_type": "海景大床房", "price": 599, "stock": 3}
动态生成语音：“今日海景大床房特价599元，仅剩3间！”

自动化建议
用 crontab（Linux） 或 Windows 任务计划程序 每小时运行一次
在 ai_voice_rotator.py 中加入 current_price.mp3 到轮播列表
OBS 场景中单独添加一个音频源播放此文件（实现“价格播报”）
"""
import os
import requests
import dashscope
from dashscope import TextToSpeech
from datetime import datetime

# === 配置 ===
DASHSCOPE_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
PMS_API_URL = "https://your-pms.com/api/v1/today-price"  # 替换为你的 PMS 接口
OUTPUT_PATH = "ai_hotel_live/audio/current_price.mp3"

dashscope.api_key = DASHSCOPE_API_KEY

def get_today_price():
    """从 PMS 获取今日价格（示例）"""
    # 实际项目中替换为真实认证 & 请求
    resp = requests.get(PMS_API_URL, timeout=5)
    data = resp.json()
    return data["room_type"], data["price"], data["stock"]

def generate_price_voice():
    try:
        room_type, price, stock = get_today_price()
        ssml = f'''
        <speak>
        今日<emphasis level="moderate">{room_type}</emphasis>，
        直播间专享价<prosody pitch="high" rate="slow">{price}元</prosody>！
        <break time="400ms"/>
        库存仅剩<prosody pitch="high">{stock}间</prosody>，
        抢完即止！
        </speak>
        '''.strip()

        response = TextToSpeech.call(
            model='sambert-zhichu-v1',
            voice='zhichu_emo',
            text=ssml,
            sample_rate=24000,
            format='mp3'
        )

        if response.status_code == 200:
            with open(OUTPUT_PATH, 'wb') as f:
                f.write(response.output.audio_data)
            print(f"[{datetime.now().strftime('%H:%M')}] 已更新价格语音: {price}元, {stock}间")
        else:
            print("TTS 生成失败:", response.message)

    except Exception as e:
        print("PMS 或 TTS 错误:", e)

if __name__ == "__main__":
    generate_price_voice()