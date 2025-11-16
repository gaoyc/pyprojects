"""
首先需要在抖音开放平台完成以下步骤
"""
# config.py - 配置文件
DOUYIN_CONFIG = {
    "client_key": "你的应用Key",      # 从开放平台获取
    "client_secret": "你的应用Secret", # 从开放平台获取
    "redirect_uri": "你的回调地址",    # 在开放平台配置的回调地址
    "scopes": ["item.list", "data.external.item"]  # 需要的权限范围
}