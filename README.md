# 微信公众号推送工具 (WeChat MP Publisher)

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)]()

一个轻量的微信公众号草稿推送工具。把 Markdown 文章推送到公众号草稿箱，支持图片自动上传、封面图永久素材、HTML 渲染。

## 功能特性

- **Markdown → HTML**：支持表格、代码块、引用、加粗、链接等常用格式
- **图片自动上传**：文章内所有图片自动上传到微信 CDN，替换外链
- **封面图永久素材**：封面通过永久素材接口上传，确保草稿创建成功
- **access_token 自动管理**：缓存自动刷新，过期前提前更新
- **环境变量配置**：凭证不写代码，通过环境变量注入

## 安装

```bash
git clone <repository-url>
cd wechat-mp-publish
pip install requests
```

## 配置

### 第一步：获取 AppID 和 AppSecret

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入 **设置与开发 → 基本配置**
3. 找到 **AppID** 和 **AppSecret**（如未生成，点击"启用"后查看）

> 注意：AppSecret 只有一次完整展示的机会，请截图保存。

### 第二步：配置白名单

在同一页面找到 **IP白名单**，将本机 IP 加入白名单。
本机 IP：`192.168.0.102`（内网）或使用 https://ip.sb 查看公网 IP。

### 第三步：设置环境变量

```bash
export WECHAT_APPID="your_appid"
export WECHAT_APPSECRET="your_appsecret"
```

### 方式二：命令行配置（首次）

```bash
python scripts/config.py <AppID> <AppSecret>
# 示例：python scripts/config.py wx1234567890abcdef abcdef1234567890abcdef
```

> ⚠️ 首次配置后 `scripts/config.json` 会保存凭证，**请勿提交到版本库**。

## 使用

### 命令行推送

```bash
python scripts/publish.py \
  --title "文章标题" \
  --content "/path/to/article.md" \
  --author "作者名" \
  --digest "摘要（不填自动生成）" \
  --cover "/path/to/cover.jpg"
```

### 集成到其他工具

```python
import subprocess

result = subprocess.run([
    "python", "scripts/publish.py",
    "--title", "文章标题",
    "--content", "/path/to/article.md",
    "--author", "作者",
    "--cover", "/path/to/cover.jpg"
], capture_output=True, text=True)
print(result.stdout)
```

## 文件结构

```
wechat-mp-publish/
├── SKILL.md              # OpenClaw Skill 定义
├── scripts/
│   ├── config.py         # 凭证配置
│   ├── token_manager.py  # access_token 管理
│   ├── image_uploader.py # 图片上传（临时素材）
│   ├── cover_uploader.py # 封面上传（永久素材）
│   ├── html_renderer.py  # Markdown → HTML
│   ├── html_sanitizer.py # HTML 清洗
│   └── publish.py        # 主编脚本
├── README.md
├── VERSION
└── CHANGELOG.md
```

## 工作流程

```
配置 AppID/AppSecret
        ↓
   获取 access_token（自动缓存）
        ↓
   上传文章图片 → 替换 HTML 中的图片 URL
        ↓
   上传封面图 → 获取 media_id
        ↓
   渲染 Markdown → HTML
        ↓
   创建草稿 → 完成
```

## 个人账号限制

- ✅ **支持**：推送到草稿箱
- ❌ **不支持**：直接群发、获取公众号数据（阅读量、用户分析等）、调用已发布相关的 API
- 个人订阅号 API 权限非常有限，如需完整功能需升级为认证服务号

## 常见问题

| 问题 | 解决方法 |
|------|---------|
| 返回 40001 | access_token 无效，检查 AppID/AppSecret |
| 图片上传失败 | 检查 IP 是否在公众号后台白名单 |
| 草稿创建成功但后台看不到 | 确认 AppID 有草稿箱权限 |
| 报"content has error" | HTML 中有微信不接受的标签，已自动清洗 |

## 相关项目

- [bazi-skill](https://github.com/NickY4ng/bazi-skill) - 八字命理分析Skill
