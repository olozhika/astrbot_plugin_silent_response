# Astrbot沉默以应插件[APSR]
# Astrbot Silent Response Plugin

为AI赋予“沉默权”：基于对话逻辑自动判断话题边界，在对话自然结束或内容无意义时，通过输出特定内容触发插件函数吞掉回复，以达到不回复用户的效果，彻底避免无限复读与尬聊

Empowering AI with the "Right to Silence": Intelligently detects conversation boundaries based on dialogue logic, and voluntarily ceases responses when topics conclude or interactions become unproductive. Breaks the endless chat loop.

## ✨ 功能特性

- **智能判断**：通过注入系统提示词，引导 AI 识别对话终点。
- **静默拦截**：当 AI 输出预设的触发词（如 `[SILENCE]`）时，插件会自动吞掉该条回复，用户端不会收到任何消息。且用户之前的信息仍能正常记入聊天历史。
- **高度可配置**：支持自定义触发词和引导语。

## 🛠️ 使用指南

在 AstrBot 插件市场下载安装即可，理论上你并不需要更改本插件的任何设置。

### 使用演示


## ⚙️ 配置项说明
理论上你并不需要更改本插件的任何设置。对于安装了某些自动修改AI回复内容的插件的用户，可考虑开启`stop_event_on_silence`。

- `silence_trigger`: AI 选择沉默时输出的特定字符串，默认触发词为 `[SILENCE]`。
- `system_instruction`: 告诉 AI 何时该沉默的指令，你可以根据 AI 的实际表现调整这段指令。
- `enable_auto_instruction`: 是否自动注入上述指令。本项关闭后AI将完全不知道如何闭嘴。
- `stop_event_on_silence`: 当触发沉默时，是否停止后续插件对响应的处理，默认关闭。开启后可防止其他插件在已拦截的回复后追加内容。
