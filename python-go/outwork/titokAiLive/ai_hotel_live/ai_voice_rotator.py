import os
import shutil
import time
import random
from datetime import datetime

# === 关键修复：使用绝对路径 ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # 脚本所在目录
AUDIO_SOURCE_DIR = os.path.join(SCRIPT_DIR, "audio", "sources")
CURRENT_AUDIO_PATH = os.path.join(SCRIPT_DIR, "audio", "current.mp3")

SCRIPTS = [
    # "01_welcome.mp3",
    # "02_seaview_room.mp3",
    # "03_promo.mp3",
    # "04_pet_faq.mp3",
    # "05_nearby.mp3",
    # "06_closing.mp3"

    "01-开场.MP3",
    "02-房型介绍01-望舒浴缸露台亲子房.MP3",
    "02-房型介绍02-西景双卧家庭套房.MP3",
    "03-周边推荐.MP3",
    "04-收尾促单.MP3"
]

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def main():
    log("AI语音轮播脚本启动...")
    while True:
        chosen = random.choice(SCRIPTS)
        source_path = os.path.join(AUDIO_SOURCE_DIR, chosen)
        if not os.path.exists(source_path):
            log(f"警告：{chosen} 不存在")
            time.sleep(30)
            continue
        try:
            # 复制前记录原文件信息（用于验证）
            before_size = os.path.getsize(CURRENT_AUDIO_PATH) if os.path.exists(CURRENT_AUDIO_PATH) else 0
            before_mtime = os.path.getmtime(CURRENT_AUDIO_PATH) if os.path.exists(CURRENT_AUDIO_PATH) else 0

            # 文件仍使用原有时间戳
            # shutil.copy2(source_path, CURRENT_AUDIO_PATH)

            # 方法1：先 copy 内容，再 touch 更新时间为 now
            shutil.copy(source_path, CURRENT_AUDIO_PATH)  # 只复制内容，不保留原时间戳
            # 强制更新访问时间和修改时间为当前时间
            now = time.time()
            os.utime(CURRENT_AUDIO_PATH, (now, now))

            # 验证是否真的更新了
            after_size = os.path.getsize(CURRENT_AUDIO_PATH)
            after_mtime = os.path.getmtime(CURRENT_AUDIO_PATH)

            if after_mtime > before_mtime or after_size != before_size:
                log(f"✅ 已切换话术: {chosen} | 文件大小: {after_size} bytes")
            else:
                log(f"⚠️ 文件未更新？源: {source_path} -> 目标: {CURRENT_AUDIO_PATH}")

            # # 测试播放
            # from playsound import playsound  # playsound 是一个跨平台的库，可以播放 MP3 和 WAV 文件。它不需要其他依赖库
            # # 播放音乐文件
            # playsound('test.mp3')

            # from pydub import AudioSegment
            # from pydub.playback import play
            # # 加载和播放 WAV 文件
            # # song = AudioSegment.from_wav(CURRENT_AUDIO_PATH)
            # song = AudioSegment.from_mp3(CURRENT_AUDIO_PATH)
            # play(song)

        except Exception as e:
            log(f"复制失败：{e}")
        time.sleep(random.randint(20, 120))

if __name__ == "__main__":
    main()
