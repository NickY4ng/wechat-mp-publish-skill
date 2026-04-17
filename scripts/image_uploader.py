#!/usr/bin/env python3
"""
微信公众号图片上传
- 上传本地图片到微信 CDN，返回 url
- 缓存已上传图片，避免重复上传
"""

import json
import os
import hashlib
import requests
from token_manager import get_access_token

CACHE_FILE = os.path.join(os.path.dirname(__file__), "image_cache.json")


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def upload_image(image_path: str) -> str:
    """上传图片到微信 CDN，返回 url"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片不存在: {image_path}")

    # 检查缓存（用文件 md5 做 key）
    with open(image_path, "rb") as f:
        file_hash = hashlib.md5(f.read()).hexdigest()

    cache = load_cache()
    if file_hash in cache:
        print(f"  [缓存命中] {image_path}")
        return cache[file_hash]

    # 上传
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={token}&type=image"

    with open(image_path, "rb") as f:
        files = {"media": (os.path.basename(image_path), f, "image/jpeg")}
        resp = requests.post(url, files=files, timeout=30)

    data = resp.json()
    if "url" not in data:
        raise Exception(f"图片上传失败: {data}")

    # 写入缓存
    cache[file_hash] = data["url"]
    save_cache(cache)
    print(f"  [上传成功] {image_path} -> {data['url']}")
    return data["url"]


def upload_image_from_url(image_url: str) -> str:
    """下载网络图片并上传到微信 CDN"""
    cache = load_cache()
    if image_url in cache:
        print(f"  [URL缓存命中] {image_url}")
        return cache[image_url]

    # 下载图片
    resp = requests.get(image_url, timeout=15)
    resp.raise_for_status()

    token = get_access_token()
    upload_url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={token}&type=image"

    from io import BytesIO
    files = {"media": ("image.jpg", BytesIO(resp.content), "image/jpeg")}
    upload_resp = requests.post(upload_url, files=files, timeout=30)
    data = upload_resp.json()

    if "url" not in data:
        raise Exception(f"URL图片上传失败: {data}")

    cache[image_url] = data["url"]
    save_cache(cache)
    print(f"  [上传成功] {image_url} -> {data['url']}")
    return data["url"]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python image_uploader.py <图片路径>")
        sys.exit(1)
    url = upload_image(sys.argv[1])
    print(f"图片URL: {url}")
