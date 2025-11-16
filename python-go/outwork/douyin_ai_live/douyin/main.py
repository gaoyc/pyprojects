# main.py - 完整使用流程
from auth import DouyinAuth
from product_api import DouyinProductAPI
from product_manager import ProductManager


def main():
    # 1. 初始化认证
    auth = DouyinAuth()

    # 2. 获取授权URL（让民宿主扫码）
    auth_url = auth.get_auth_url()
    print(f"请让民宿主扫码授权: {auth_url}")

    # 3. 用户授权后获取授权码（这里需要实际从回调获取）
    auth_code = input("请输入授权成功后获取的code: ")

    # 4. 获取access_token和open_id
    access_token, open_id = auth.get_access_token(auth_code)
    if not access_token:
        print("授权失败!")
        return

    # 5. 初始化商品API
    product_api = DouyinProductAPI(access_token, open_id)

    # 6. 获取所有商品
    all_products = product_api.get_all_products()

    # 7. 保存商品数据
    product_manager = ProductManager()
    product_manager.save_products(all_products)

    # 8. 获取适合直播的商品
    live_products = product_manager.get_products_for_live()
    print(f"找到 {len(live_products)} 个适合直播的商品")

    # 9. 导出数据
    product_manager.export_to_json()

    # 打印商品信息
    for product in live_products[:5]:  # 显示前5个
        print(f"商品: {product['title']}")
        print(f"价格: {product['price']}元")
        print(f"库存: {product['stock']}")
        print("-" * 50)


if __name__ == "__main__":
    main()