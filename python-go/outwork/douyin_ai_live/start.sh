#!/bin/bash
# start.sh

echo "🚀 抖音AI直播系统 - 一键启动 (Linux/macOS)"

# 检查 .env 是否存在
if [ ! -f ".env" ]; then
    echo "❌ 错误: 请先创建 .env 配置文件！"
    echo "参考模板:"
    echo "DASHSCOPE_API_KEY=sk-xxxx"
    echo "ALIYUN_ACCESS_KEY_ID=LTAIxxxx"
    echo "ALIYUN_ACCESS_KEY_SECRET=xxxx"
    echo "OBS_PASSWORD=your_obs_password (如设置了)"
    exit 1
fi

# 加载 .env 到环境变量（供 docker-compose 使用）
export $(cat .env | xargs)

# 创建 audio 目录
mkdir -p audio

# 启动服务
echo "🐳 正在构建并启动容器..."
docker-compose up --build

echo "✅ 服务已停止"