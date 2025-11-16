# auth.py - 认证模块
import requests
import json
from config import DOUYIN_CONFIG


class DouyinAuth:
    def __init__(self):
        self.client_key = DOUYIN_CONFIG["client_key"]
        self.client_secret = DOUYIN_CONFIG["client_secret"]
        self.redirect_uri = DOUYIN_CONFIG["redirect_uri"]
        self.base_url = "https://open.douyin.com"

    def get_auth_url(self):
        """生成授权URL，让民宿主扫码授权"""
        scopes = ",".join(DOUYIN_CONFIG["scopes"])
        auth_url = (f"{self.base_url}/platform/oauth/connect/"
                    f"?client_key={self.client_key}"
                    f"&response_type=code"
                    f"&scope={scopes}"
                    f"&redirect_uri={self.redirect_uri}")
        return auth_url

    def get_access_token(self, auth_code):
        """通过授权码获取access_token"""
        url = f"{self.base_url}/oauth/access_token/"
        data = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }

        try:
            response = requests.post(url, data=data)
            result = response.json()

            if result.get("data"):
                access_token = result["data"]["access_token"]
                open_id = result["data"]["open_id"]
                print(f"授权成功! open_id: {open_id}")
                return access_token, open_id
            else:
                print(f"获取token失败: {result}")
                return None, None

        except Exception as e:
            print(f"请求token异常: {e}")
            return None, None

    def refresh_token(self, refresh_token):
        """刷新access_token"""
        url = f"{self.base_url}/oauth/refresh_token/"
        data = {
            "client_key": self.client_key,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }

        response = requests.post(url, data=data)
        return response.json()