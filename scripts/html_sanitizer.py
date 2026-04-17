#!/usr/bin/env python3
"""
微信公众号 HTML 清洗
- 微信会过滤违规标签和样式
- 删除 class、id、position:fixed、float 等
"""

import re


def sanitize_html(html: str) -> str:
    """清洗 HTML，移除微信不支持的标签和属性"""
    # 移除 class 属性
    html = re.sub(r'\s*class="[^"]*"', '', html)
    # 移除 id 属性
    html = re.sub(r'\s*id="[^"]*"', '', html)
    # 移除 style 中的 position:fixed 和 float
    html = re.sub(r'position\s*:\s*fixed[^;]*;?', '', html, flags=re.IGNORECASE)
    html = re.sub(r'float\s*:\s*[^;]+;?', '', html, flags=re.IGNORECASE)
    # 清理空白属性
    html = re.sub(r'\s+', ' ', html)
    return html.strip()


if __name__ == "__main__":
    test = '<div class="test" id="foo" style="position:fixed; float:left;">hello</div>'
    print(sanitize_html(test))
