"""
OBS 控制模块（obs_controller.py）

OBS 设置指南：

安装 OBS WebSocket 插件
OBS → 工具 → WebSocket 服务器设置 → 启用（端口 4455）
添加一个 媒体源，名称设为 AI_Voice（与 OBS_SOURCE_NAME 一致）
初始文件可任选（会被脚本覆盖）
"""
# obs_controller.py
import os
from dotenv import load_dotenv
from obsws_python import ReqClient

load_dotenv()

OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", "4455"))
OBS_PASSWORD = os.getenv("OBS_PASSWORD", "")
OBS_SOURCE_NAME = os.getenv("OBS_SOURCE_NAME", "AI_Voice")

def switch_obs_audio_source(file_path: str):
    """切换OBS媒体源路径"""
    try:
        with ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3) as cl:
            cl.set_input_settings(
                input_name=OBS_SOURCE_NAME,
                input_settings={"local_file": os.path.abspath(file_path)},
                overlay=True
            )
        print(f"✅ OBS媒体源 '{OBS_SOURCE_NAME}' 已切换到: {file_path}")
    except Exception as e:
        print(f"❌ OBS切换失败: {e}")
        raise