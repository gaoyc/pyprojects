"""
自动重启推流（防断流）
"""

# monitor_obs.py
import psutil
import time
import os

def is_obs_running():
    return any("obs" in p.name().lower() for p in psutil.process_iter())

def restart_obs():
    os.system("taskkill /f /im obs64.exe")
    time.sleep(2)
    os.startfile(r"C:\Program Files\obs-studio\bin\64bit\obs64.exe")

while True:
    if not is_obs_running():
        print("OBS 已退出，正在重启...")
        restart_obs()
    time.sleep(60)