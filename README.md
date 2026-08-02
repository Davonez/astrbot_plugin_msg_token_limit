# astrbot_plugin_msg_token_limit

群聊消息长度（Token）限制插件 —— 超长消息自动拦截并提示，防止刷屏。

基于 [AstrBot](https://github.com/Soulter/AstrBot) 框架开发。

**作者：Davonez**

## ✨ 功能特性

- 🚫 **超长消息自动拦截**：艾特机器人（或唤醒指令）的消息若超过设定的 token 上限，将被拦截，不会继续传播给后续插件 / LLM，有效防止刷屏。
- 🧮 **智能 Token 估算**：中文字符按约 1.5 token / 字估算，其他字符按约 0.3 token / 字符估算，无需引入额外依赖。
- 🎯 **按群生效**：可配置只对指定群启用限制，留空则所有群生效。
- ⭐ **白名单机制**：指定的 QQ 用户不受限制，方便管理员 / 机器人所有者自由发言。
- 💬 **自定义提示语**：超长提示语支持占位符 `{max_tokens}`，可自由定制文案。

## 📦 安装

1. 将本插件目录（`astrbot_plugin_msg_token_limit`）放入 AstrBot 的 `plugins` 目录下；
2. 在 AstrBot 管理面板中**重载插件**；
3. 按需修改插件配置（见下文）。

## ⚙️ 配置说明

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `max_tokens` | `int` | `100` | 每个用户单条消息允许的最大 token 数。中文约 1.5 token/字，100 token 大约等于 60~70 个汉字 |
| `enabled_groups` | `list` | `[]` | 启用限制的群号列表，留空表示所有群生效。例如 `["123456789"]` |
| `whitelist_users` | `list` | `[]` | 白名单用户 QQ，这些用户不受限制 |
| `tip_message` | `string` | `⚠️ 消息太长啦，请控制在 {max_tokens} token 以内喵~` | 超长消息提示语，`{max_tokens}` 会被替换成实际上限值 |

## 🧠 工作原理

1. 收到群消息后，仅对**艾特机器人（或唤醒指令）**的消息进行检查；
2. 若配置了 `enabled_groups`，则只对列表内的群生效；
3. 白名单用户直接跳过检查；
4. 通过简易估算函数计算消息 token 数：

   ```python
   tokens = 中文字符数 × 1.5 + 其他字符数 × 0.3
   ```

5. 若超过 `max_tokens`，发送提示语并 `stop_event()` 拦截该消息，不再继续传播。

## 📄 文件结构

```
astrbot_plugin_msg_token_limit/
├── main.py            # 插件主逻辑
├── metadata.yaml      # 插件元数据
├── _conf_schema.json  # 配置项 Schema
└── README.md          # 本文档
```

## 📝 更新日志

### v1.0.0

- 首个版本，实现群消息 token 长度限制、白名单、按群生效、自定义提示语等核心功能。

## 📜 许可证

本项目采用 **MIT License** 开源。
