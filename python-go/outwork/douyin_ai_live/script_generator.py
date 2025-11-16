"""
Qwen 话术生成
"""
# script_generator.py
import os
from dotenv import load_dotenv
from dashscope import Generation

load_dotenv()

def generate_script(product_info: dict) -> str:
    prompt = f"""
你是一位专业抖音带货主播，请根据以下商品信息，生成一段30秒左右的直播口播文案。
要求：
- 语气热情、有感染力，带紧迫感（如“手慢无”“库存不多”）
- 突出价格优势、核心卖点、适用人群
- 引导点击小黄车下单
- 不要使用“大家好”“今天我们来介绍”等开场白
- 纯文本，不要加任何markdown或符号

商品信息：
标题：{product_info['title']}
价格：{product_info['price']}（原价{product_info['original_price']}）
销量：{product_info['sales']}
核心卖点：{', '.join(product_info['features'])}
描述：{product_info['description']}
""".strip()

    response = Generation.call(
        model="qwen-max",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        prompt=prompt,
        temperature=0.7,
        max_tokens=250,
        top_p=0.8
    )
    if response.status_code == 200:
        text = response.output.text.strip()
        # 过滤可能的违禁词（示例）
        text = text.replace("最", "超").replace("第一", "热门")
        return text
    else:
        raise RuntimeError(f"Qwen生成失败: {response.code} - {response.message}")


