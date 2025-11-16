"""
Web 界面 + API（app.py）
✅ Web 界面输入商品链接：提供一个简易网页，用户粘贴抖音商品链接后自动触发 AI 生成 + 播放。
✅ OBS 自动切换播放：通过 WebSocket 动态加载新生成的音频文件，实现无缝播放；

# 启动 Flask Web 服务
python app.py

启动后，浏览器访问：http://localhost:5000

抖音商品链接（或直接输入商品ID用于测试），点击“生成并播放”，系统将：

生成话术；
调用阿里云TTS；
保存 MP3 到 audio/；
自动通知 OBS 切换到新音频；
OBS 立即开始播放新内容（旧音频不会中断，因为文件未被修改）。
"""
# app.py
import os
import time
import threading
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
from product_parser import fetch_product_info_by_id
from script_generator import generate_script
from tts_aliyun import ali_tts
from obs_controller import switch_obs_audio_source

app = Flask(__name__)
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# 简易前端页面
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>抖音AI直播助手</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 40px auto; padding: 20px; }
        input[type=url] { width: 100%; padding: 10px; margin: 10px 0; }
        button { background: #ff2d55; color: white; border: none; padding: 12px 20px; cursor: pointer; }
        button:disabled { background: #ccc; }
        .log { background: #f5f5f5; padding: 10px; margin-top: 20px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h2>抖音AI直播助手</h2>
    <p>请输入抖音商品分享链接（如 https://v.douyin.com/xxxxx）</p>
    <form id="form">
        <input type="url" id="url" placeholder="https://v.douyin.com/..." required>
        <button type="submit">生成并播放</button>
    </form>
    <div class="log" id="log"></div>

    <script>
        const form = document.getElementById('form');
        const log = document.getElementById('log');
        form.onsubmit = async (e) => {
            e.preventDefault();
            const url = document.getElementById('url').value;
            const btn = form.querySelector('button');
            btn.disabled = true;
            log.innerHTML += '[INFO] 正在处理...\\n';
            try {
                const res = await fetch('/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                const data = await res.json();
                if (res.ok) {
                    log.innerHTML += `[SUCCESS] ${data.message}\\n`;
                } else {
                    log.innerHTML += `[ERROR] ${data.error}\\n`;
                }
            } catch (err) {
                log.innerHTML += `[EXCEPTION] ${err.message}\\n`;
            }
            btn.disabled = false;
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/generate', methods=['POST'])
def generate_and_play():
    data = request.get_json()
    short_url = data.get("url", "").strip()

    if not short_url:
        return jsonify({"error": "请提供商品链接"}), 400

    # 从链接提取商品ID（简化：假设用户直接输入ID或完整goods链接）
    # 实际可调用 resolve_douyin_link(short_url) 解析
    try:
        if "goods/" in short_url:
            product_id = short_url.split("goods/")[-1].split("?")[0].split("/")[0]
        else:
            product_id = short_url  # 假设直接输入ID用于测试
        product = fetch_product_info_by_id(product_id)
    except Exception as e:
        return jsonify({"error": f"商品解析失败: {str(e)}"}), 400

    # 在后台线程执行耗时任务（避免HTTP超时）
    def background_task():
        try:
            script = generate_script(product)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 生成话术: {script}")

            output_path = os.path.join(AUDIO_DIR, f"live_{int(time.time())}.mp3")
            ali_tts(script, output_path)

            # 通知 OBS 切换
            switch_obs_audio_source(output_path)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] OBS已切换至: {output_path}")
        except Exception as e:
            print(f"[ERROR] 后台任务失败: {e}")

    threading.Thread(target=background_task, daemon=True).start()
    return jsonify({"message": "任务已提交，正在生成语音..."})


# ... [前面的 import 和路由定义保持不变] ...
# @app.route('/generate', methods=['POST'])
# def generate_and_play():
#     # ... [你的逻辑] ...
#     threading.Thread(target=background_task, daemon=True).start()
#     return jsonify({"message": "任务已提交，正在生成语音..."})

# ===== 必须添加这一段！=====
if __name__ == '__main__':
    print("🚀 启动 Flask Web 服务，访问 http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)