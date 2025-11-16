"""
获取商品信息
"""
# product_api.py - 商品API接口
import requests
import json
import time
from datetime import datetime, timedelta


class DouyinProductAPI:
    def __init__(self, access_token, open_id):
        self.access_token = access_token
        self.open_id = open_id
        self.base_url = "https://open.douyin.com"
        self.headers = {
            "Content-Type": "application/json",
            "access-token": access_token
        }

    def get_product_list(self, page=0, size=20, status=0):
        """
        获取商品列表
        status: 0-上架, 1-下架, 2-审核中
        """
        url = f"{self.base_url}/api/douyin/trade/v2/product/query/"

        params = {
            "open_id": self.open_id,
            "page": page,
            "size": size,
            "status": status
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            result = response.json()

            if result.get("data"):
                products = result["data"]["products"]
                print(f"获取到 {len(products)} 个商品")
                return products
            else:
                print(f"获取商品列表失败: {result.get('message')}")
                return []

        except Exception as e:
            print(f"请求商品列表异常: {e}")
            return []

    def get_product_detail(self, product_id):
        """获取商品详情"""
        url = f"{self.base_url}/api/douyin/trade/v2/product/detail/"

        params = {
            "open_id": self.open_id,
            "product_id": product_id
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            result = response.json()

            if result.get("data"):
                return result["data"]
            else:
                print(f"获取商品详情失败: {result.get('message')}")
                return None

        except Exception as e:
            print(f"请求商品详情异常: {e}")
            return None

    def get_all_products(self):
        """获取所有商品（分页获取）"""
        all_products = []
        page = 0
        size = 50  # 每页最大数量

        while True:
            print(f"正在获取第 {page + 1} 页商品...")
            products = self.get_product_list(page=page, size=size)

            if not products:
                break

            all_products.extend(products)

            # 如果返回数量小于请求数量，说明已经是最后一页
            if len(products) < size:
                break

            page += 1
            time.sleep(0.5)  # 避免请求过快

        print(f"共获取 {len(all_products)} 个商品")
        return all_products

    def get_product_statistics(self, product_ids, start_date=None, end_date=None):
        """
        获取商品数据统计
        需要 data.external.item 权限
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        url = f"{self.base_url}/data/external/item/base/"

        stats_data = []
        for product_id in product_ids:
            params = {
                "open_id": self.open_id,
                "item_id": product_id,
                "date_type": 7  # 近30天
            }

            try:
                response = requests.get(url, headers=self.headers, params=params)
                result = response.json()

                if result.get("data"):
                    stats_data.append({
                        "product_id": product_id,
                        "stats": result["data"]
                    })
                else:
                    print(f"获取商品 {product_id} 统计失败")

            except Exception as e:
                print(f"获取商品统计异常: {e}")

            time.sleep(0.2)  # 控制请求频率

        return stats_data