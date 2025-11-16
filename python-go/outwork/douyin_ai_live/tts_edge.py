"""
TTS语音合成（两种方案任选）
方案A：免费 - Edge TTS（微软）
"""
# tts_edge.py
import edge_tts
import asyncio

async def text_to_speech_edge(text: str, output_path: str):
    communicate = edge_tts.Communicate(text, voice="zh-CN-XiaoxiaoNeural")
    await communicate.save(output_path)