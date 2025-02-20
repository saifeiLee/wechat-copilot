# wechat-copilot

自动解析微信窗口的聊天内容,结合 AI 大模型，生成回复建议。

![演示](docs/demo.gif)

## 核心思路

1. 使用 `pyobjc` 获取微信窗口的聊天内容
2. 使用 `openai` 的 API 生成回复建议
3. 使用 `osascript` 生成系统通知
4. 使用 `pyperclip` 自动复制到剪贴板

## 本地启动

### 环境准备

```bash
brew install uv
uv venv
source .venv/bin/activate
uv pip install --editable .
touch .env
```

填写环境变量到.env文件

```bash
# 填写你的 openai api key
OPENAI_API_KEY=
# 填写你的 openai base url
OPENAI_BASE_URL=
```

### 运行

```bash
python src/main.py
```
### 使用

1. 打开微信聊天窗口
2. 快捷键：`cmd+shift+space` 触发
3. GPT 会根据聊天内容生成回复建议，以系统通知的方式展示，自动复制到剪贴板
4. 粘贴文本到聊天框，自行决定二次编辑


---
喜欢的话，可以点个 🌟star🌟 支持一下。感谢感谢。