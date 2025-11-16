# main.py
"""
# 运行命令:
# python main.py 123456789
"""
import os
import sys
from datetime import datetime
from product_parser import fetch_product_info_by_id
from script_generator import generate_script
from tts_aliyun import ali_tts

OUTPUT_DIR = "audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def main():
    if len(sys.argv) < 2:
        print("用法: python main.py <商品ID>")
        print("示例: python main.py 123456789")
        return

    product_id = sys.argv[1].strip()
    log(f"🔍 正在获取商品: {product_id}")

    # 1. 获取商品信息
    product = fetch_product_info_by_id(product_id)

    # 2. 生成话术
    log("🧠 正在生成AI话术...")
    script = generate_script(product)
    log(f"🎙️ 话术: {script}")

    # 3. TTS合成
    output_path = os.path.join(OUTPUT_DIR, f"live_{int(time.time())}.mp3")
    log("🔊 正在调用阿里云TTS...")
    ali_tts(script, output_path)

    log("✅ 全流程完成！音频已生成，可在OBS中播放。")

if __name__ == "__main__":
    import time
    main()