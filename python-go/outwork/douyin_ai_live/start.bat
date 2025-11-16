@echo off
REM start.bat

echo 🚀 抖音AI直播系统 - 一键启动 (Windows)

IF NOT EXIST .env (
    echo ❌ 错误: 请先创建 .env 配置文件！
    echo 参考模板:
    echo DASHSCOPE_API_KEY=sk-xxxx
    echo ALIYUN_ACCESS_KEY_ID=LTAIxxxx
    echo ALIYUN_ACCESS_KEY_SECRET=xxxx
    echo OBS_PASSWORD=your_obs_password (如设置了)
    pause
    exit /b 1
)

REM 创建 audio 目录
if not exist audio mkdir audio

REM 启动
echo 🐳 正在构建并启动容器...
docker-compose up --build

pause