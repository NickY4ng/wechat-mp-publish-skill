#!/usr/bin/env python3
"""
微信公众号文章发布脚本
流程：
1. 读取 Markdown 文章
2. 上传文章图片到微信 CDN
3. 上传封面到永久素材
4. 渲染 Markdown → HTML
5. 创建草稿到公众号草稿箱
"""

import json
import os
import re
import sys
import requests
from datetime import datetime

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(__file__))
from token_manager import get_access_token
from image_uploader import upload_image, upload_image_from_url
from cover_uploader import upload_cover
from html_renderer import render_markdown, replace_images_in_html


def extract_images_from_markdown(md: str):
    """提取 Markdown 中的所有图片路径和 URL"""
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    images = []
    for match in re.finditer(pattern, md):
        alt, url = match.group(1), match.group(2)
        images.append((url, alt))
    return images


def upload_all_images(md: str):
    """上传所有图片，返回 {原始URL: 微信CDN_URL} 映射"""
    images = extract_images_from_markdown(md)
    if not images:
        return {}

    print(f"发现 {len(images)} 张图片，开始上传...")
    image_map = {}

    for url, alt in images:
        try:
            if url.startswith("http"):
                new_url = upload_image_from_url(url)
            else:
                new_url = upload_image(url)
            image_map[url] = new_url
        except Exception as e:
            print(f"  [跳过] {url}: {e}")

    return image_map


def create_draft(title: str, author: str, content: str, digest: str, cover_media_id: str):
    """创建草稿到公众号草稿箱"""
    token = get_access_token()
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"

    payload = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "thumb_media_id": cover_media_id,
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }
        ]
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}

    resp = requests.post(url, data=data, headers=headers, timeout=30)
    result = resp.json()

    if result.get("errcode", 0) != 0:
        raise Exception(f"创建草稿失败: {result}")

    print(f"  [草稿创建成功] media_id: {result.get('media_id')}")
    return result


def publish_article(title: str, author: str, md_content: str, digest: str, cover_path: str = None):
    """
    发布文章到公众号草稿箱
    """
    print(f"开始发布文章: {title}")
    print("=" * 40)

    # 1. 上传文章图片
    print("\n[1/4] 上传文章图片...")
    image_map = upload_all_images(md_content)

    # 2. 上传封面
    print("\n[2/4] 上传封面图...")
    if cover_path and os.path.exists(cover_path):
        cover_media_id = upload_cover(cover_path)
    elif cover_path:
        print(f"  [警告] 封面图不存在: {cover_path}，跳过")
        cover_media_id = ""
    else:
        print("  [跳过] 未指定封面图")
        cover_media_id = ""

    # 3. 渲染 HTML 并替换图片
    print("\n[3/4] 渲染 HTML...")
    html_content = render_markdown(md_content, author)
    if image_map:
        html_content = replace_images_in_html(html_content, image_map)
    print(f"  HTML 长度: {len(html_content)} 字符")

    # 4. 创建草稿
    print("\n[4/4] 创建草稿...")
    result = create_draft(title, author, html_content, digest, cover_media_id)

    print("\n" + "=" * 40)
    print(f"✅ 发布成功！")
    print(f"   标题: {title}")
    print(f"   草稿ID: {result.get('media_id')}")
    print(f"   请到公众号后台 -> 草稿箱 -> 发布")

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="发布文章到微信公众号草稿箱")
    parser.add_argument("--title", required=True, help="文章标题")
    parser.add_argument("--content", required=True, help="Markdown 文件路径 或 直接传 Markdown 文本")
    parser.add_argument("--author", default="", help="作者")
    parser.add_argument("--digest", default="", help="摘要")
    parser.add_argument("--cover", default="", help="封面图路径")

    args = parser.parse_args()

    # 读取内容
    content = args.content
    if os.path.exists(content):
        with open(content) as f:
            content = f.read()
        if len(content.strip()) < 10:
            print(f"❌ 文件内容为空或过短")
            sys.exit(1)
        print(f"已从文件读取，内容长度: {len(content)} 字符")
    else:
        # content 不是有效文件路径，当作直接传 Markdown 文本处理
        if len(content.strip()) < 10:
            print(f"❌ 文章内容为空或过短，请检查输入")
            sys.exit(1)
        print(f"使用直接传入的 Markdown 内容，长度: {len(content)} 字符")

    # 自动生成摘要
    if not args.digest and content:
        # 取前100字作为摘要
        text = re.sub(r'[#*!\[\]()>`\n]', '', content)
        digest = text[:100] + "..." if len(text) > 100 else text
    else:
        digest = args.digest

    try:
        publish_article(
            title=args.title,
            author=args.author,
            md_content=content,
            digest=digest,
            cover_path=args.cover if os.path.exists(args.cover) else None
        )
    except Exception as e:
        print(f"\n❌ 发布失败: {e}")
        sys.exit(1)
