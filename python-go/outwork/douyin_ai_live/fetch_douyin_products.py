"""
[抖音开放平台](https://developer.open-douyin.com/)

1、前往抖音开放平台注册开发者账号并创建应用，申请所需API权限。
2、获取访问令牌，用于调用商品列表API。
3、调用API接口，它将返回包含商品ID、名称、价格、图片等信息的JSON数据。
"""
# coding:utf-8
import requests
import json


def fetch_douyin_products(access_token, keyword=None, page=1, page_size=20):
    """
    获取抖音商品列表
    """
    # 构造API请求URL，这里以商品搜索为例，具体 endpoint 请查阅最新官方文档
    url = "https://open.douyin.com/api/v2/product/search/"

    # 准备请求头，携带认证信息
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 准备请求参数，可根据官方文档调整
    params = {
        "page": page,
        "page_size": page_size
    }
    if keyword:
        params["keyword"] = keyword  # 若需按关键词筛选商品则可传入

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()

        # 解析返回的JSON数据，此处字段名请以官方API返回为准
        if data.get("code") == 0:  # 或 success
            products = data["data"]["items"]
            print(f"成功获取 {len(products)} 个商品")
            return products
        else:
            print(f"API返回错误: {data.get('message')}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"请求商品API时出错: {e}")
        return []

# 使用示例 (需将 YOUR_ACCESS_TOKEN 替换为你的实际令牌)
# products = fetch_douyin_products("YOUR_ACCESS_TOKEN")
# for product in products:
#     print(f"商品名: {product.get('title')}, 价格: {product.get('price')}")

"""
请注意：上述代码中的API端点（url）和返回数据的解析方式（例如data["data"]["items"]）为示例性质。在实际开发中，请务必以抖音开放平台最新的官方API文档为准，因为接口路径和返回字段可能会发生变化。
"""