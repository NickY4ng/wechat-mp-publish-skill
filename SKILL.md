---
name: wechat-mp-publish
version: v1.0.0
description: 微信公众号推送工具。将 Markdown 文章推送到公众号草稿箱，支持图片自动上传、封面图永久素材、HTML渲染。触发词：推送公众号、发布公众号、发到微信。
---

# 微信公众号推送工具 (WeChat MP Publisher)

## 功能

1. 自动获取 access_token（支持环境变量配置）
2. 上传文章中所有图片到微信 CDN
3. 上传封面图到永久素材
4. 将 Markdown 渲染为微信 HTML
5. 创建草稿到公众号草稿箱

## 使用前配置

### 环境变量（推荐）

```bash
export WECHAT_APPID="your_appid"
export WECHAT_APPSECRET="your_appsecret"
```

### 命令行配置

```bash
python scripts/config.py <AppID> <AppSecret>
```

> ⚠️ 运行后会生成 `scripts/config.json`，请确保不提交到版本库（已加入 .gitignore）

## 使用方式

### 命令行发布

```bash
python scripts/publish.py \
  --title "文章标题" \
  --content "/path/to/article.md" \
  --author "作者名" \
  --digest "摘要（不填则自动截取）" \
  --cover "/path/to/cover.jpg"
```

## API 原理

```
access_token → 上传图片 → 上传封面 → 创建草稿
    ↓            ↓           ↓          ↓
  自动刷新     替换URL    获取media  JSON POST
```

## 重要说明

- **content 参数**：推荐传 Markdown 文件路径，脚本会自动读取文件内容
- **封面用永久素材**：封面图必须用永久素材接口，否则创建草稿会失败
- **中文编码**：POST 时使用 `ensure_ascii=False` + UTF-8
- **敏感信息**：请勿提交 `config.json` 和 `token_store.json`

## 文件结构
```
├── SKILL.md
├── scripts/
│   ├── config.py
│   ├── token_manager.py
│   ├── image_uploader.py
│   ├── cover_uploader.py
│   ├── html_renderer.py
│   ├── html_sanitizer.py
│   └── publish.py
├── README.md
├── VERSION
├── CHANGELOG.md
└── .gitignore
```
