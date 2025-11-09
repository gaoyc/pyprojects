# ai_voice_rotator_smooth.py
"""
pip install mutagen obsws-python

脚本选中一个 MP3 文件；
自动读取它的播放时长（秒）；
播放后，精确等待该时长，再切换下一条；
配合前面的 双缓冲 + OBS WebSocket 切换，实现丝滑无中断轮播。

配置 OBS
在 OBS 场景中添加一个 媒体源；
名称设为 AI_Voice_Audio（必须和代码中的 MEDIA_SOURCE_NAME 一致）；
初始文件可任选一个（如 buffer_a.mp3），但之后会被脚本覆盖；
取消勾选 “循环”（除非你希望单条音频循环）；
确保没有勾选“本地文件”下的“重新连接”之类选项。
💡 OBS 会在每次切换路径后，从头开始播放新文件，但因为旧文件已播完（或接近播完），所以听感自然。

"""
import os
import time
import random
from datetime import datetime
from mutagen.mp3 import MP3
import shutil
try:
    import obsws_python as obsws
except ImportError:
    raise RuntimeError("请安装: pip install obsws-python")

# === 配置 ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_SOURCE_DIR = os.path.join(SCRIPT_DIR, "audio", "sources")
AUDIO_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "audio")

BUFFER_A = os.path.join(AUDIO_OUTPUT_DIR, "buffer_a.mp3")
BUFFER_B = os.path.join(AUDIO_OUTPUT_DIR, "buffer_b.mp3")

OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = ""
MEDIA_SOURCE_NAME = "AI_Voice_Audio"  # 必须与 OBS 中媒体源名称一致

SCRIPTS = [
    "01-开场.MP3",
    "02-房型介绍01-望舒浴缸露台亲子房.MP3",
    "02-房型介绍02-西景双卧家庭套房.MP3",
    "03-周边推荐.MP3",
    "04-收尾促单.MP3"
]

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def get_mp3_duration(file_path: str) -> float:
    try:
        audio = MP3(file_path)
        return audio.info.length
    except Exception as e:
        log(f"⚠️ 读取时长失败 {file_path}: {e}")
        return 0.0

def copy_audio(src, dst):
    with open(src, 'rb') as f:
        data = f.read()
    tmp = dst + ".tmp"
    with open(tmp, 'wb') as f:
        f.write(data)
    os.replace(tmp, dst)

def switch_obs_media(client, file_path):
    try:
        client.set_input_settings(
            input_name=MEDIA_SOURCE_NAME,
            input_settings={"local_file": file_path},
            overlay=True
        )
        log(f"✅ OBS 切换至: {os.path.basename(file_path)}")
    except Exception as e:
        log(f"❌ OBS 切换失败: {e}")

def main():
    log("🔊 AI语音轮播（精准时长等待模式）启动...")
    os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

    # 校验源文件 & 预读时长（可选缓存）
    script_durations = {}
    for f in SCRIPTS:
        src = os.path.join(AUDIO_SOURCE_DIR, f)
        if not os.path.isfile(src):
            log(f"❌ 缺失文件: {f}")
            return
        dur = get_mp3_duration(src)
        script_durations[f] = dur
        log(f"📁 {f} | 时长: {dur:.1f} 秒")

    # 连接 OBS
    try:
        cl = obsws.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)
        log("✅ OBS WebSocket 已连接")
    except Exception as e:
        log(f"❌ OBS 连接失败: {e}")
        return

    current_buffer = BUFFER_A
    next_buffer = BUFFER_B

    # 播放第一条
    first = random.choice(SCRIPTS)
    src_path = os.path.join(AUDIO_SOURCE_DIR, first)
    copy_audio(src_path, current_buffer)
    switch_obs_media(cl, current_buffer)
    duration = script_durations[first]
    log(f"▶️ 开始播放: {first} ({duration:.1f}s)")

    try:
        while True:
            # 精准等待当前音频播放完毕
            if duration > 0:
                log(f"⏳ 等待 {duration:.1f} 秒后切换...")
                time.sleep(duration + 0.5)  # +0.5秒缓冲，确保播完
            else:
                # 如果无法获取时长，保守等待 30 秒
                time.sleep(30)

            # 选择下一条
            chosen = random.choice(SCRIPTS)
            src_path = os.path.join(AUDIO_SOURCE_DIR, chosen)
            duration = script_durations[chosen]

            # 更新备用缓冲区
            copy_audio(src_path, next_buffer)
            log(f"🔄 预载完成: {chosen} ({duration:.1f}s)")

            # 切换 OBS
            switch_obs_media(cl, next_buffer)

            # 交换缓冲区
            current_buffer, next_buffer = next_buffer, current_buffer

    except KeyboardInterrupt:
        log("🛑 用户终止")
    finally:
        cl.disconnect()

if __name__ == "__main__":
    main()