#!/usr/bin/env python3
"""
Markdown → 微信 HTML 渲染器
- 将 Markdown 转换为带内联样式的 HTML
- 微信不支持外部 CSS，所有样式必须内联
"""

import re
import markdown
from html_sanitizer import sanitize_html


def render_markdown(md: str, author: str = "") -> str:
    """
    将 Markdown 渲染为微信可用的 HTML
    - 使用 markdown 库转基本 HTML
    - 替换图片 src 为微信 CDN URL（由调用方预先替换）
    """
    # 基本 Markdown → HTML
    html = markdown.markdown(
        md,
        extensions=["tables", "fenced_code", "codehilite"]
    )

    # 包裹整体，添加基础样式
    header = ""
    if author:
        header = f'<p style="color:#888;font-size:12px;margin-bottom:20px;">作者：{author}</p>'

    # 为 img 标签添加样式
    def style_img(match):
        img = match.group(0)
        if 'style="' not in img:
            img = img.replace("<img ", '<img style="max-width:100%;height:auto;display:block;margin:10px 0;" ')
        return img

    html = re.sub(r'<img[^>]+>', style_img, html)

    # 为 table 添加样式
    html = html.replace("<table>", '<table style="border-collapse:collapse;width:100%;margin:15px 0;">')
    html = html.replace("<th>", '<th style="background:#f5f5f5;padding:8px;border:1px solid #ddd;text-align:left;font-weight:bold;">')
    html = html.replace("<td>", '<td style="padding:8px;border:1px solid #ddd;">')
    html = html.replace("<tr>", '<tr style="border-bottom:1px solid #eee;">')

    # 清理 p 标签
    def style_p(match):
        p = match.group(0)
        if 'style="' not in p:
            p = p.replace("<p>", '<p style="line-height:1.8;margin:10px 0;">')
        return p

    html = re.sub(r'<p[^>]*>.*?</p>', style_p, html, flags=re.DOTALL)

    # 清理并返回
    html = sanitize_html(html)

    return f'''{header}{html}'''


def replace_images_in_html(html: str, image_map: dict) -> str:
    """替换 HTML 中的图片 src（image_map: {原始URL: 微信CDN_URL}）"""
    for old_url, new_url in image_map.items():
        html = html.replace(f'src="{old_url}"', f'src="{new_url}"')
        html = html.replace(f"src='{old_url}'", f"src='{new_url}'")
    return html


if __name__ == "__main__":
    test_md = """# 标题

这是一段正文。

![图片描述](https://example.com/test.jpg)

## 二级标题

- 列表项1
- 列表项2

```
代码块
```
"""
    print(render_markdown(test_md))
