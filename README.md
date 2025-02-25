# wechat-copilot

自动解析微信窗口的聊天内容,结合 AI 大模型，生成回复建议。

喜欢的话可以点个 🌟star🌟 支持一下。感谢感谢。

## 感谢

项目方案的灵感离不开以下开源项目的启发：

- https://github.com/browser-use/macOS-use

![演示](docs/demo.gif)

## 快速安装

```bash
pip install wechat-copilot
```

## 配置

1. 创建配置文件:

```bash
mkdir -p ~/.wechat-copilot
touch ~/.wechat-copilot/config.env
```

2. 编辑配置文件 `~/.wechat-copilot/config.env`:

```bash
# 必填：OpenAI API密钥
OPENAI_API_KEY=your_key_here

# 可选：OpenAI API地址（默认为 https://api.openai.com/v1）
OPENAI_BASE_URL=https://api.openai.com/v1

# 可选：快捷键设置（默认为 cmd+shift+space）
SHORTCUT=cmd+shift+space
```

## 使用方法

1. 运行助手:

```bash
wechat-copilot
```

2. 打开微信聊天窗口
3. 快捷键：`cmd+shift+space` 触发
4. GPT 会根据聊天内容生成回复建议，以系统通知的方式展示，自动复制到剪贴板
5. 粘贴文本到聊天框，自行决定二次编辑

## 开发者指南

如果你想参与开发:

```bash
git clone https://github.com/yourusername/wechat-copilot.git
cd wechat-copilot
pip install -e ".[dev]"
```

## 核心思路

1. 使用 `pyobjc` 获取微信窗口的聊天内容
2. 使用 `openai` 的 API 生成回复建议
3. 使用 `osascript` 生成系统通知
4. 使用 `pyperclip` 自动复制到剪贴板

## 构建发布

```bash
python -m build
twine upload dist/*
```
---

喜欢的话，可以点个 🌟star🌟 支持一下。感谢感谢。

---

## FAQ

**Q:** 发布到pypi遇到报错: InvalidDistribution: Metadata is missing required fields: Name, Version.

**A:** 需要更新pkginfo

```bash
pip install --upgrade pkginfo
```

