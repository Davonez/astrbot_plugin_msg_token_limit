import sys
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.config.astrbot_config import AstrBotConfig
from astrbot.core.message.message_event_result import MessageChain


@register(
    "astrbot_plugin_msg_token_limit",
    "Davonez",
    "群聊消息长度(token)限制：超长消息自动拦截并提示，防止刷屏。",
    "1.0.0",
)
class MsgTokenLimit(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        # 每个用户单条消息允许的最大 token 数
        self.max_tokens = int(config.get("max_tokens", 100))
        # 启用限制的群号列表，留空表示所有群都生效
        self.enabled_groups = config.get("enabled_groups", [])
        # 白名单用户 QQ，这些用户不受限制
        self.whitelist = config.get("whitelist_users", [])
        # 超长提示语（{max_tokens} 会被替换成实际上限）
        self.tip_message = config.get(
            "tip_message", "⚠️ 消息太长啦，请控制在 {max_tokens} token 以内喵~"
        )

    def _estimate_tokens(self, text: str) -> float:
        """简易 token 估算：中文字符约 1.5 token，其他字符约 0.3 token"""
        if not text:
            return 0.0
        chinese = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
        other = len(text) - chinese
        return chinese * 1.5 + other * 0.3

    @filter.event_message_type(
        filter.EventMessageType.GROUP_MESSAGE, priority=sys.maxsize - 1
    )
    async def on_group_message(self, event: AstrMessageEvent):
        try:
            # 只有艾特机器人（或唤醒指令）的消息才检查长度限制
            if not event.is_at_or_wake_command:
                return

            text = event.get_message_str() or ""
            if not text:
                return

            # 群限制开关：只对配置中的群生效
            if self.enabled_groups:
                group_id = event.get_group_id()
                if group_id and str(group_id) not in [str(g) for g in self.enabled_groups]:
                    return

            # 白名单用户跳过
            sender_id = event.get_sender_id()
            if sender_id and str(sender_id) in [str(u) for u in self.whitelist]:
                return

            # 估算 token 数并拦截超长消息
            tokens = self._estimate_tokens(text)
            if tokens > self.max_tokens:
                tip = self.tip_message.format(max_tokens=self.max_tokens)
                await event.send(MessageChain().message(tip))
                event.stop_event()  # 拦截该消息，不再继续传播给后续插件/LLM
        except Exception as e:
            logger.error(f"[msg_token_limit] 处理消息异常: {e}")
