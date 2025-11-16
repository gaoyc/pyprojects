"""
自动生成产品介绍话术
获取到原始商品数据后，我们可以使用大语言模型来为每个商品生成生动有趣的口播文案。这里以调用 OpenAI GPT 系列模型的 API 为例。
核心思路： 构建一个清晰的提示词，将商品信息、民宿特色以及你希望的话术风格传递给模型。
"""
import openai  # 需要先安装: pip install openai
def generate_product_script(product_info, hotel_theme="海滨度假民宿"):
    """
    根据商品信息生成AI口播文案
    """
    # 构造一个详细的提示词
    prompt = f"""
    你是一名专业的民宿直播主播，正在为自家酒店进行推广。
    请根据以下商品信息，生成一段适合抖音直播场景、充满吸引力的口播文案，要求口语化、有感染力，并突出商品卖点，长度在100字左右。

    **商品信息:**
    - 名称: {product_info.get('title', 'N/A')}
    - 价格: {product_info.get('price', 'N/A')}元
    - 图片/描述关键词: {product_info.get('image_urls', [])} {product_info.get('description', '暂无详细描述')}

    **民宿主题:** {hotel_theme}

    **请开始生成口播文案:**
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 也可选用 "gpt-4"
            messages=[
                {"role": "system", "content": "你是一个风趣幽默的民宿直播主播。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.8  # 控制创造性，可根据需要调整
        )
        script = response.choices[0].message.content.strip()
        return script
    except Exception as e:
        print(f"生成话术时出错: {e}")
        return f"大家好，今天给大家推荐 {product_info.get('title')}，价格非常优惠，只要 {product_info.get('price')} 元，千万不要错过哦！"

# 使用示例 (需设置你的OPENAI_API_KEY环境变量)
# product_example = {"title": "豪华海景房一晚住宿", "price": 888, "image_urls": ["sea_view.jpg"]}
# script = generate_product_script(product_example)
# print(script)