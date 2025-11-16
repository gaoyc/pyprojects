"""
阿里云TTS集成
"""
# tts_aliyun.py
import os
import time
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from dotenv import load_dotenv

load_dotenv()

def ali_tts(text: str, output_file: str):
    """
    使用阿里云TTS将文本转为MP3语音
    文档: https://help.aliyun.com/document_detail/459880.html
    """
    client = AcsClient(
        os.getenv("ALIYUN_ACCESS_KEY_ID"),
        os.getenv("ALIYUN_ACCESS_KEY_SECRET"),
        "cn-shanghai"  # TTS服务区域，必须与控制台一致
    )

    request = CommonRequest()
    request.set_domain("nls-meta.cn-shanghai.aliyuncs.com")
    request.set_version("2019-08-27")
    request.set_action_name("SubmitTtsTask")

    request.add_query_param("Text", text)
    request.add_query_param("Voice", os.getenv("TTS_VOICE", "zhimiao_emo"))
    request.add_query_param("SampleRate", int(os.getenv("TTS_SAMPLE_RATE", "16000")))
    request.add_query_param("Format", os.getenv("TTS_FORMAT", "mp3"))
    request.add_query_param("Volume", int(os.getenv("TTS_VOLUME", "50")))
    request.add_query_param("SpeechRate", int(os.getenv("TTS_SPEECH_RATE", "0")))
    request.add_query_param("PitchRate", int(os.getenv("TTS_PITCH_RATE", "0")))

    try:
        response = client.do_action_with_exception(request)
        result = json.loads(response)
        task_id = result["TaskId"]
        print(f"✅ TTS任务提交成功，TaskId: {task_id}")

        # 轮询获取结果（最多等待60秒）
        for _ in range(60):
            time.sleep(1)
            url = get_tts_result(client, task_id)
            if url:
                # 下载音频
                import requests
                audio_data = requests.get(url).content
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"🎧 音频已保存: {output_file}")
                return
        raise TimeoutError("TTS合成超时")
    except Exception as e:
        raise RuntimeError(f"阿里云TTS失败: {e}")

def get_tts_result(client, task_id: str):
    """查询TTS任务结果"""
    request = CommonRequest()
    request.set_domain("nls-meta.cn-shanghai.aliyuncs.com")
    request.set_version("2019-08-27")
    request.set_action_name("GetTtsResult")
    request.add_query_param("TaskId", task_id)
    response = client.do_action_with_exception(request)
    result = json.loads(response)
    if result.get("Status") == "SUCCESS":
        return result.get("AudioUrl")
    return None