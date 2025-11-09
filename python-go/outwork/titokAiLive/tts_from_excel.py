"""
从 Excel 读取话术并批量生成 MP3

Excel 格式要求（scripts.xlsx）
filename	text (支持纯文本或 SSML)
01_welcome.mp3	<speak>欢迎...
02_seaview...	<speak>这款海景...

依赖：
pip install pandas openpyxl dashscope

"""
import os
import pandas as pd
import dashscope
from dashscope import TextToSpeech
import time

# === 配置 ===
""" DASHSCOPE_API_KEY环境变量设置
set DASHSCOPE_API_KEY=sk-xxxx  # Windows
export DASHSCOPE_API_KEY=sk-xxxx  # Linux/macOS
"""
# DASHSCOPE_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

EXCEL_PATH = "scripts.xlsx"  # 话术表
OUTPUT_DIR = "ai_hotel_live/audio/sources"
os.makedirs(OUTPUT_DIR, exist_ok=True)

dashscope.api_key = DASHSCOPE_API_KEY


def text_to_speech(text, output_path):
    try:
        response = TextToSpeech.call(
            model='sambert-zhichu-v1',
            voice='zhichu_emo',
            text=text,
            sample_rate=24000,
            format='mp3'
        )
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.output.audio_data)
            print(f"✅ {os.path.basename(output_path)}")
        else:
            print(f"❌ 失败: {response.code} - {response.message}")
    except Exception as e:
        print(f"🔥 异常: {e}")
    time.sleep(0.8)  # 防 QPS 超限


# === 主程序 ===
if __name__ == "__main__":
    df = pd.read_excel(EXCEL_PATH)
    for _, row in df.iterrows():
        filename = str(row["filename"]).strip()
        text = str(row["text"]).strip()
        if not filename.endswith(".mp3"):
            filename += ".mp3"
        output_path = os.path.join(OUTPUT_DIR, filename)
        text_to_speech(text, output_path)

    print(f"\n🎉 共生成 {len(df)} 条语音，路径：{os.path.abspath(OUTPUT_DIR)}")