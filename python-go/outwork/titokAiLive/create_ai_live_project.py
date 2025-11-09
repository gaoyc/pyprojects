import os
import base64
from PIL import Image
from pydub import AudioSegment


def create_placeholder_image(path, color=(200, 220, 240), size=(1280, 720)):
    img = Image.new("RGB", size, color)
    img.save(path)


def create_silent_mp3(path, duration_ms=1000):
    silent = AudioSegment.silent(duration=duration_ms)
    #silent.export(path, format="mp3") # 注意生成mp3格式需要系统安装ffmpeg，改用 .wav 格式（无需 ffmpeg）
    silent.export(path, format="wav") #注意生成mp3格式需要系统安装ffmpeg，改用 .wav 格式（无需 ffmpeg）

def main():
    project_root = "ai_hotel_live"  # d:/ai_hotel_live
    os.makedirs(project_root, exist_ok=True)

    # 创建 images 文件夹
    img_dir = os.path.join(project_root, "images")
    os.makedirs(img_dir, exist_ok=True)
    create_placeholder_image(os.path.join(img_dir, "room1.jpg"), (220, 240, 220))
    create_placeholder_image(os.path.join(img_dir, "room2.jpg"), (220, 230, 250))
    create_placeholder_image(os.path.join(img_dir, "exterior.jpg"), (200, 220, 240))
    create_placeholder_image(os.path.join(img_dir, "promo_banner.png"), (255, 240, 200))

    # 创建 audio 文件夹
    audio_dir = os.path.join(project_root, "audio")
    sources_dir = os.path.join(audio_dir, "sources")
    os.makedirs(sources_dir, exist_ok=True)

    # 创建 current.mp3（空）
    create_silent_mp3(os.path.join(audio_dir, "current.mp3"))

    # 创建话术占位 MP3
    scripts = [
        "01_welcome.mp3",
        "02_seaview_room.mp3",
        "03_promo.mp3",
        "04_pet_faq.mp3",
        "05_nearby.mp3",
        "06_closing.mp3"
    ]
    for script in scripts:
        create_silent_mp3(os.path.join(sources_dir, script))

    # OBS 配置模板
    obs_config = '''{
  "version": "32.0.2",
  "sources": [
    {
      "name": "Mujing_Background",
      "type": "slideshow",
      "settings": {
        "files": [
          {"value": "C:/live/images/room1.jpg"},
          {"value": "C:/live/images/room2.jpg"},
          {"value": "C:/live/images/exterior.jpg"},
          {"value": "C:/live/images/breakfast.jpg"}
        ],
        "slide_time": 8000,
        "randomize": true,
        "loop": true
      }
    },
    {
      "name": "AI_Voice_Audio",
      "type": "vlc_source",
      "settings": {
        "playlist": [
          {"value": "file:///C:/live/audio/current.mp3"}
        ],
        "loop": true,
        "autoplay": true
      }
    },
    {
      "name": "Dynamic_Time",
      "type": "text_gdiplus_v2",
      "settings": {
        "text": "%Y-%m-%d %H:%M",
        "font": {"face": "微软雅黑", "size": 24},
        "color": 16777215,
        "outline": true,
        "outline_color": 0
      }
    },
    {
      "name": "Promo_Sticker",
      "type": "image_source",
      "settings": {
        "file": "C:/live/images/promo_banner.png"
      }
    }
  ],
  "scenes": [
    {
      "name": "AI_Hotel_Live",
      "id": 1,
      "sources": [
        {"name": "Mujing_Background"},
        {"name": "AI_Voice_Audio"},
        {"name": "Dynamic_Time"},
        {"name": "Promo_Sticker"}
      ]
    }
  ]
}'''
    with open(os.path.join(project_root, "obs_template.json"), "w", encoding="utf-8") as f:
        f.write(obs_config)

    # Python 轮播脚本
    rotator_script = '''import os
import shutil
import time
import random
from datetime import datetime

AUDIO_SOURCE_DIR = r"audio/sources"
CURRENT_AUDIO_PATH = r"audio/current.mp3"

SCRIPTS = [
    "01_welcome.mp3",
    "02_seaview_room.mp3",
    "03_promo.mp3",
    "04_pet_faq.mp3",
    "05_nearby.mp3",
    "06_closing.mp3"
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
            shutil.copy2(source_path, CURRENT_AUDIO_PATH)
            log(f"已切换话术：{chosen}")
        except Exception as e:
            log(f"复制失败：{e}")
        time.sleep(random.randint(90, 120))

if __name__ == "__main__":
    main()
'''
    with open(os.path.join(project_root, "ai_voice_rotator.py"), "w", encoding="utf-8") as f:
        f.write(rotator_script)

    # README
    readme = """# AI 民宿直播项目

## 使用步骤
1. 将你的民宿图片放入 `images/`，替换占位图
2. 用剪映生成 AI 语音 MP3，放入 `audio/sources/`，命名如 01_welcome.mp3
3. 在 OBS 中导入 `obs_template.json`
4. 运行 `ai_voice_rotator.py`
5. 推流到抖音直播伴侣

注意：OBS 中的路径需根据你的实际项目位置修改！
"""
    with open(os.path.join(project_root, "README.txt"), "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"✅ 项目已创建成功！路径：{os.path.abspath(project_root)}")
    print("📌 请按 README.txt 中的步骤操作")


if __name__ == "__main__":
    # 安装依赖（首次运行需要）
    try:
        from PIL import Image
        from pydub import AudioSegment
    except ImportError:
        print("正在安装依赖：pillow, pydub...")
        os.system("pip install pillow pydub")
        from PIL import Image
        from pydub import AudioSegment
    main()