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

### 第一步：获取 AppID 和 AppSecret

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入 **设置与开发 → 基本配置**
3. 找到 **AppID** 和 **AppSecret**（如未生成，点击"启用"后查看）

> 注意：AppSecret 只有一次完整展示的机会，请截图保存。

### 第二步：配置白名单

1. 在同一页面（**设置与开发 → 基本配置 → 公众号开发者密码**）
2. 找到 **IP白名单**，将本机 IP 加入白名单
3. 本机 IP 为：`192.168.0.102`（如需查询公网 IP，请访问 ip.sb 或 ifconfig.me）

### 第三步：配置环境变量

```bash
export WECHAT_APPID="your_appid"
export WECHAT_APPSECRET="your_appsecret"
```

或使用命令行配置：

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

## 重要说明

### 个人账号限制

- ✅ **支持**：推送到草稿箱
- ❌ **不支持**：直接群发、获取公众号数据（阅读量、用户分析等）、调用已发布相关的 API
- 个人订阅号 API 权限非常有限，如需完整功能需升级为认证服务号

### 其他注意事项

- **content 参数**：推荐传 Markdown 文件路径，脚本会自动读取文件内容
- **封面用永久素材**：封面图必须用永久素材接口，否则创建草稿会失败
- **敏感信息**：请勿提交 `config.json` 和 `token_store.json`
- **图片上传**：所有图片自动上传到微信 CDN，无需手动处理

## API 原理

```
access_token → 上传图片 → 上传封面 → 创建草稿
    ↓            ↓           ↓          ↓
  自动刷新     替换URL    获取media  JSON POST
```

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
