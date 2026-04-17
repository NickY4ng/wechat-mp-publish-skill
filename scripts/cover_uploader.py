#!/usr/bin/env python3
"""
微信公众号封面上传（永久素材）
- 封面图必须用永久素材接口，返回 media_id
"""

import os
import json
import requests
from token_manager import get_access_token


def upload_cover(cover_path: str) -> str:
    """上传封面图到永久素材，返回 media_id"""
    if not os.path.exists(cover_path):
        raise FileNotFoundError(f"封面图不存在: {cover_path}")

    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"

    with open(cover_path, "rb") as f:
        files = {"media": (os.path.basename(cover_path), f, "image/jpeg")}
        resp = requests.post(url, files=files, timeout=30)

    data = resp.json()
    if "media_id" not in data:
        raise Exception(f"封面上传失败: {data}")

    print(f"  [封面上传成功] media_id: {data['media_id']}")
    return data["media_id"]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python cover_uploader.py <封面图路径>")
        sys.exit(1)
    media_id = upload_cover(sys.argv[1])
    print(f"media_id: {media_id}")
