from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.provider import ProviderRequest

@register("silent_response", "olozhika", "为AI赋予沉默权，避免无意义复读与尬聊", "1.0.0")
class SilentResponsePlugin(Star):
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.config = config or {}

    @filter.on_llm_request()
    async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
        """注入沉默指令"""
        if not self.config.get("enable_auto_instruction", True):
            return
        instruction = self.config.get("system_instruction", "")
        trigger = self.config.get("silence_trigger", "[SILENCE]")
        if instruction:
            final_instruction = instruction.replace("[SILENCE]", trigger)
            req.system_prompt += f"\n\n【系统指令 - 沉默权】\n{final_instruction}\n"

    @filter.on_llm_response()
    async def on_llm_response(self, event: AstrMessageEvent, resp):
        """拦截沉默触发词，并手动保存对话历史"""
        trigger = self.config.get("silence_trigger", "[SILENCE]")
        if resp.completion_text.strip() == trigger:
            logger.info(f"[APSR] 检测到沉默触发词 {trigger}，已拦截回复。")

            # 获取对话管理器
            conv_mgr = self.context.conversation_manager
            umo = event.unified_msg_origin
            cid = await conv_mgr.get_curr_conversation_id(umo)  # 获取当前对话ID
            if cid:
                # 构造消息字典（OpenAI 格式）
                user_message = {"role": "user", "content": event.message_str}
                assistant_message = {"role": "assistant", "content": ""}
                # 使用 add_message_pair 将这一对消息追加到历史中
                await conv_mgr.add_message_pair(cid, user_message, assistant_message)

            # 清空实际回复内容，这样用户不会收到任何消息
            resp.completion_text = ""
            # 停止事件传播，防止其他插件干扰 (尤其适用于用户装了很多功能复杂的插件时）
            if self.config.get("stop_event_on_silence", False):
                event.stop_event()
