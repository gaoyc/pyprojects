"""
主控脚本（整合流程）

后续与直播集成（OBS）
在 OBS 中添加 媒体源，路径设为 live_voice.mp3；
运行脚本后，新语音会覆盖该文件；
但为避免中断，建议用前文“双缓冲 + WebSocket 切换”方案；
或者每次生成不同文件名（如 voice_1712345678.mp3），并通过 WebSocket 动态切换路径。
"""
# live_ai_host.py
import os
import asyncio
import time
from datetime import datetime
from product_parser import resolve_douyin_link, fetch_product_info
from script_generator import generate_script
from tts_edge import text_to_speech_edge

AUDIO_OUTPUT = "live_voice.mp3"


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


async def main():
    # 1. 输入商品链接（可改为队列或API）
    short_url = input("请输入抖音商品分享链接: ").strip()

    # 2. 解析商品
    product_id = resolve_douyin_link(short_url)
    product = fetch_product_info(product_id)
    log(f"✅ 商品: {product['title']}")

    # 3. 生成话术
    script = generate_script(product)
    log(f"🎙️ 话术: {script}")

    # 4. 合成语音
    log("🔊 正在合成语音...")
    await text_to_speech_edge(script, AUDIO_OUTPUT)
    log(f"🎧 语音已保存: {AUDIO_OUTPUT}")

    # 5. 播放（可集成OBS或推流）
    # 方式1: 手动在OBS中添加 media source 指向 live_voice.mp3
    # 方式2: 自动通过 obs-websocket 切换（见前文）
    # 方式3: 用 ffplay 播放（测试用）
    os.system(f"ffplay -nodisp -autoexit {AUDIO_OUTPUT}")


if __name__ == "__main__":
    asyncio.run(main())