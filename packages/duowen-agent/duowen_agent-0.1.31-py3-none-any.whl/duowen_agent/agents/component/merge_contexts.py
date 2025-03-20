from typing import List

from pydantic import BaseModel, Field

from duowen_agent.llm import Message, MessagesSet
from duowen_agent.llm.chat_model import OpenAIChat
from duowen_agent.llm.utils import format_messages
from duowen_agent.prompt.prompt_build import GeneralPromptBuilder, practice_dir
from duowen_agent.utils.core_utils import json_observation
from duowen_agent.utils.string_template import StringTemplate


class AnalysisResult(BaseModel):
    theme_switch_points: List[str] = Field(
        ..., description="对话中的主题切换点，通常是一些关键的对话片段"
    )
    filtered_content: str = Field(..., description="经过筛选后与新问题相关的内容")


class AnalysisOutput(BaseModel):
    analysis_result: AnalysisResult = Field(
        ..., description="分析结果，包含主题切换点和筛选内容"
    )
    new_question: str = Field(..., description="基于筛选内容生成的逻辑连贯的新问题")


class MergeContexts:
    def __init__(self, llm_instance: OpenAIChat):
        self.llm_instance = llm_instance

    def run(self, question: List[dict] | List[Message] | MessagesSet):
        _question = format_messages(question)
        _history = [i.to_dict() for i in _question.message_list[:-1]]
        _history_content = "\n\n".join(
            [f'{i["role"]}:\n{i["content"]}' for i in _history]
        )
        _new = _question.message_list[-1]
        _prompt = GeneralPromptBuilder.load("merge_contexts").get_instruction(
            user_input=f"- 历史对话内容:\n```\n{_history_content}\n```\n\n- 最新消息:\n```\n{_new.content}\n```"
        )

        res = self.llm_instance.chat(_prompt)
        res: AnalysisOutput = json_observation(res, AnalysisOutput)
        return res.new_question


class Continued(BaseModel):
    is_continued: bool = Field(description="存在话题延续性为true否则为false")


class TopicContinues:

    def __init__(self, llm_instance: OpenAIChat):
        self.llm_instance = llm_instance

    @staticmethod
    def build_prompt():
        GeneralPromptBuilder(
            instruction=StringTemplate(
                template="分析用户最新消息与之前{num}轮对话内容，判断是否存在话题延续性。",
            ),
            step=StringTemplate(
                template="""1. **追溯对话历史**：
   - 提取最近{num}轮对话内容（包括用户当前消息）
   - 重点标记用户当前消息
2. **识别关键要素**：
   - 操作指令词库匹配（请/帮我/需要...）
   - 社交寒暄模式识别（问候/感谢/客套话）
   - 代词指代消解（这/那/它等上下文绑定）
   - 包含任务参数延续（时间/地点/数量的渐进调整）
3. **排除非延续情况**：
   - 纯社交性表达（类似"谢谢"_"您好"_"麻烦了"等）
   - 跳转至完全无关话题领域
4. **逻辑链验证**：
   - 检查当前消息是否服务于同一任务目标
   - 确认存在观点延伸/条件补充/细节深挖等延续特征
   - 辨别是否出现逆向推理链（质疑反驳/否定前提）""",
            ),
            output_format=Continued,
            note="""1. 特别注意"这/那+量词"结构的隐性指代（如"那个方案"_"这份文件"）
2. 关注时间序列关联（"上次"_"之前"_"刚才"_"接下来"）
3. 警惕伪装延续场景（表面相似但语义断裂的情况）
3. 当出现复合意图时（如闲聊中带请求），需要特别评估请求是否存在延续性
4. 对于模糊指代需通过上下文验证真实指涉对象""",
        ).export_yaml(practice_dir + "/topic_continues_check.yaml")

    def run(self, question: List[dict] | List[Message] | MessagesSet, num: int = 3):
        _question = format_messages(question)
        _history = [i.to_dict() for i in _question.message_list[:-1]]
        _history_content = "\n\n".join(
            [f'消息_{e+1} {i["role"]}:\n{i["content"]}' for e, i in enumerate(_history)]
        )
        _new = _question.message_list[-1]
        _prompt = GeneralPromptBuilder.load("topic_continues_check").get_instruction(
            user_input=f"- 历史对话内容:\n```\n{_history_content}\n```\n\n- 最新消息:\n```\n{_new.content}\n```",
            temp_vars={"num": num},
        )
        res = self.llm_instance.chat(_prompt)
        res: Continued = json_observation(res, Continued)
        return res.is_continued


# class Categories(BaseModel):
#     category_name: Literal["任务延续", "话题转移", "寒暄闲聊", "模糊意图"] = Field(
#         description="Exactly the name of the category that matches"
#     )

# class MultiTurnDialogCoreIntentDetection:
#     """上下文合并"""
#
#     def __init__(self, llm_instance: OpenAIChat):
#         self.llm_instance = llm_instance
#
#     @staticmethod
#     def build_prompt():
#         GeneralPromptBuilder(
#             instruction="分析最近4轮对话内容，精准识别用户最新消息的核心意图，重点关注话题转移和寒暄场景。采用语义标记与上下文关联分析相结合的方法进行意图判别。",
#             step="""
# ## 处理流程
# 1. **对话采样**
#    - 提取最近4组交替发言
#    - 重点标记用户当前消息
#
# 2. 语义特征提取
#    - 操作指令词库匹配（请/帮我/需要...）
#    - 社交寒暄模式识别（问候/感谢/客套话）
#    - 代词指代消解（这/那/它等上下文绑定）
#
# 3. **上下文关联分析**
#    - 检查是否包含明确操作指令（任务延续）
#    - 对比前序对话主题相关性（话题转移）
#    - 识别社交礼仪表达模式（寒暄闲聊）
#    - 标注未满足分类条件的特殊表达（模糊意图）
#
# ## 分类规则
# - 任务延续条件（满足其一）： ① 含明确操作指令词 ② 代词指向前序任务要素 ③ 延续前两轮对话逻辑链
# - 话题转移标志： ① 引入全新实体对象（未在前3轮出现） ② 使用话题切换词（对了/顺便问/另外） ③ 与前序主题无语义关联
# - 寒暄闲聊特征： ① 社交礼仪模板句（你好/谢谢/再见类） ② 无具体信息请求 ③ 情感表达类陈述
#
# ## 优先级逻辑
# - 复合意图场景：操作指令词＞话题转移词＞寒暄词
# - 连续追问判定：同一主题下的3轮内细节询问
# - 模糊意图处理：标记为未分类，需补充上下文询问
# """,
#             output_format=Categories,
#             note="""
# - 当用户当前消息只存在社交寒暄模式时，优先按"寒暄闲聊"处理
# - 疑问句默认不视为话题转移，需检测是否延续前序疑问
# - 当出现复合意图时（如闲聊中带请求），优先按"任务延续"处理
# - 连续追问不视为话题转移（例：追问任务细节）
# - 聚焦用户最后一句话来识别用户的核心意图""",
#         ).export_yaml(practice_dir + "/multi_turn_dialog_core_intent_detection.yaml")
#
#     def run(self, question: List[dict] | List[Message] | MessagesSet):
#         _question = format_messages(question)
#         _history = [i.to_dict() for i in _question.message_list[:-1]]
#         _history_content = "\n\n".join(
#             [f'消息_{e+1} {i["role"]}:\n{i["content"]}' for e, i in enumerate(_history)]
#         )
#         _new = _question.message_list[-1]
#         _prompt = GeneralPromptBuilder.load(
#             "multi_turn_dialog_core_intent_detection"
#         ).get_instruction(
#             user_input=f"- 历史对话内容:\n```\n{_history_content}\n```\n\n- 最新消息:\n```\n{_new.content}\n```"
#         )
#         # print(_prompt.get_format_messages())
#         res = self.llm_instance.chat(_prompt)
#         res: Categories = json_observation(res, Categories)
#         return res.category_name


class DetectionMergeContexts:
    def __init__(self, llm_instance: OpenAIChat, **kwargs):
        self.llm_instance = llm_instance
        self.kwargs = kwargs

    def run(
        self, question: List[dict] | List[Message] | MessagesSet, num: int = 3
    ) -> str:
        _question = format_messages(question)

        res = TopicContinues(self.llm_instance).run(_question, num)

        if res:
            return MergeContexts(llm_instance=self.llm_instance).run(question)

        return _question.message_list[-1].content


if __name__ == "__main__":
    TopicContinues.build_prompt()
