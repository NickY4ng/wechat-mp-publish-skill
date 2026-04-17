#!/usr/bin/env python3
"""
微信公众号配置脚本

【开源配置】支持两种配置方式（优先读取环境变量）：

1. 环境变量（推荐）：
   export WECHAT_APPID="your_appid"
   export WECHAT_APPSECRET="your_appsecret"

2. 命令行参数（首次配置用）：
   python config.py <AppID> <AppSecret>
   → 会保存到 config.json（请勿提交 config.json 到版本库）
"""

import json
import os
import sys


def get_config_path():
    return os.path.join(os.path.dirname(__file__), "config.json")


def load_config():
    """读取配置，优先环境变量"""
    appid = os.environ.get("WECHAT_APPID")
    appsecret = os.environ.get("WECHAT_APPSECRET")
    if appid and appsecret:
        return {"appid": appid, "appsecret": appsecret}
    cfg_file = get_config_path()
    if os.path.exists(cfg_file):
        with open(cfg_file) as f:
            return json.load(f)
    return None


def save_config(appid: str, appsecret: str):
    """保存配置到 config.json"""
    cfg_file = get_config_path()
    with open(cfg_file, "w") as f:
        json.dump({"appid": appid, "appsecret": appsecret}, f, ensure_ascii=False, indent=2)
    print(f"配置已保存到 {cfg_file}")
    print(f"AppID: {appid}")
    print("请将 config.json 加入 .gitignore，勿提交到版本库")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python config.py <AppID> <AppSecret>")
        print("   或设置环境变量: WECHAT_APPID / WECHAT_APPSECRET")
        sys.exit(1)

    appid = sys.argv[1]
    appsecret = sys.argv[2]
    save_config(appid, appsecret)
