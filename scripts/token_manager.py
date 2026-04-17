#!/usr/bin/env python3
"""
微信公众号 access_token 管理
- 支持环境变量配置（WECHAT_APPID / WECHAT_APPSECRET）
- 自动缓存到 token_store.json，过期前自动刷新
"""

import json
import os
import time
import requests

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token_store.json")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def get_config():
    """读取配置，优先环境变量"""
    appid = os.environ.get("WECHAT_APPID")
    appsecret = os.environ.get("WECHAT_APPSECRET")
    if appid and appsecret:
        return {"appid": appid, "appsecret": appsecret}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    raise Exception("未找到配置：请设置环境变量 WECHAT_APPID 和 WECHAT_APPSECRET，或先运行 config.py")


def get_access_token():
    """获取 access_token，优先使用缓存，接近过期时自动刷新"""
    cfg = get_config()
    appid = cfg["appid"]
    appsecret = cfg["appsecret"]

    # 读取缓存
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE) as f:
                cached = json.load(f)
            cached_at = cached.get("cached_at", 0)
            expires_in = cached.get("expires_in", 7200)
            if time.time() - cached_at < (expires_in - 300):
                return cached["access_token"]
        except (json.JSONDecodeError, KeyError):
            pass

    # 重新获取
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": appid,
        "secret": appsecret
    }
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()

    if "access_token" not in data:
        raise Exception(f"获取 access_token 失败: {data}")

    # 缓存
    with open(TOKEN_FILE, "w") as f:
        json.dump({
            "access_token": data["access_token"],
            "expires_in": data.get("expires_in", 7200),
            "cached_at": time.time()
        }, f)

    return data["access_token"]


if __name__ == "__main__":
    try:
        token = get_access_token()
        print(f"access_token: {token[:20]}...")
    except Exception as e:
        print(f"错误: {e}")
