"""
商品数据处理和存储
"""
# product_manager.py - 商品数据管理
import json
import sqlite3
from datetime import datetime


class ProductManager:
    def __init__(self, db_path="douyin_products.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建商品表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT UNIQUE,
                title TEXT,
                price REAL,
                market_price REAL,
                stock INTEGER,
                status INTEGER,
                main_image TEXT,
                images TEXT,
                description TEXT,
                category TEXT,
                create_time DATETIME,
                update_time DATETIME,
                sales_data TEXT,
                last_sync_time DATETIME
            )
        ''')

        conn.commit()
        conn.close()

    def save_products(self, products):
        """保存商品数据到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        current_time = datetime.now().isoformat()

        for product in products:
            # 解析商品数据，字段名根据实际API返回调整
            product_data = {
                'product_id': product.get('product_id'),
                'title': product.get('title'),
                'price': product.get('price', {}).get('sale_price', 0) / 100,  # 通常以分单位
                'market_price': product.get('price', {}).get('market_price', 0) / 100,
                'stock': product.get('stock', 0),
                'status': product.get('status', 0),
                'main_image': product.get('main_image', {}).get('url', ''),
                'images': json.dumps(product.get('images', [])),
                'description': product.get('description', ''),
                'category': product.get('category_name', ''),
                'create_time': current_time,
                'update_time': current_time,
                'last_sync_time': current_time
            }

            # 插入或更新
            cursor.execute('''
                INSERT OR REPLACE INTO products 
                (product_id, title, price, market_price, stock, status, main_image, 
                 images, description, category, create_time, update_time, last_sync_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(product_data.values()))

        conn.commit()
        conn.close()
        print(f"成功保存 {len(products)} 个商品到数据库")

    def get_products_for_live(self, limit=10):
        """获取适合直播的商品"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT product_id, title, price, market_price, main_image, description, stock
            FROM products 
            WHERE status = 0 AND stock > 0  -- 上架且有库存
            ORDER BY update_time DESC
            LIMIT ?
        ''', (limit,))

        products = []
        for row in cursor.fetchall():
            products.append({
                'product_id': row[0],
                'title': row[1],
                'price': row[2],
                'market_price': row[3],
                'main_image': row[4],
                'description': row[5],
                'stock': row[6]
            })

        conn.close()
        return products

    def export_to_json(self, output_file="products.json"):
        """导出商品数据到JSON文件"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM products')
        columns = [description[0] for description in cursor.description]

        products = []
        for row in cursor.fetchall():
            product = dict(zip(columns, row))
            # 解析JSON字段
            if product.get('images'):
                product['images'] = json.loads(product['images'])
            products.append(product)

        conn.close()

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)

        print(f"商品数据已导出到 {output_file}")