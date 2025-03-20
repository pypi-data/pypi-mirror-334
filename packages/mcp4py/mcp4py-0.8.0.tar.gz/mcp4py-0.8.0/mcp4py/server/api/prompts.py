from fastapi import FastAPI, APIRouter, HTTPException
from typing import List, Optional, Dict, Union
from pydantic import BaseModel


class Argument(BaseModel):
    name: str
    description: str
    required: bool


class TextContent(BaseModel):
    type: str = "text"
    text: str


class ImageContent(BaseModel):
    type: str = "image"
    data: str  # base64 编码的图像数据
    mimeType: str


class AudioContent(BaseModel):
    type: str = "audio"
    data: str  # base64 编码的音频数据
    mimeType: str


class ResourceContent(BaseModel):
    uri: str
    mimeType: str
    text: Optional[str] = None
    data: Optional[str] = None  # base64 编码的二进制数据，如果不是文本


Content = Union[TextContent, ImageContent, AudioContent] #, ResourceContent  # 为了简化，先不包含ResourceContent


class PromptMessage(BaseModel):
    role: str  # "user" 或 "assistant"
    content: Content


class Prompt(BaseModel):
    name: str
    description: Optional[str] = None
    arguments: Optional[List[Argument]] = None


class PromptResult(BaseModel):
    description: Optional[str] = None
    messages: List[PromptMessage]

class ListPromptResponse(BaseModel):
    prompts: List[Prompt]
    nextCursor: Optional[str] = None


class Prompts(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_routes()
        self.name = "Prompts"
        self.prompts_data: Dict[str, PromptResult] = {} # 模拟prompt数据存储

    def setup_routes(self):
        router = APIRouter(prefix="/prompts", tags=["prompts"], responses={404: {"description": "未找到"}})  # 更符合文档

        @router.get("/list", response_model=ListPromptResponse)
        async def list_prompts(cursor: Optional[str] = None):
            """
            列出可用的 prompts (支持分页).
            """
            # TODO: 在实际应用中，从数据库或配置中读取 prompts 列表，并实现分页逻辑
            # 这里为了演示，返回一个硬编码的 prompts 列表
            prompts = [
                Prompt(name="code_review",
                       description="请求 LLM 分析代码质量并提出改进建议",
                       arguments=[Argument(name="code", description="要检查的代码", required=True)]),
                Prompt(name="translate",
                       description="翻译文本到指定的语言",
                       arguments=[Argument(name="text", description="要翻译的文本", required=True),
                                  Argument(name="language", description="目标语言", required=True)])
            ]
            return ListPromptResponse(prompts=prompts)  # , nextCursor="next_page") # 实际中实现nextCursor

        @router.get("/get", response_model=PromptResult)
        async def get_prompt(name: str, arguments: Optional[Dict] = None):
            """
            获取指定的 prompt.
            """
            # TODO: 从存储中检索 prompt，并根据参数生成 message
            if name == "code_review":
                code = arguments.get("code") if arguments else None
                if not code:
                    raise HTTPException(status_code=422, detail="缺少 code 参数") #Invalid params -32602
                messages = [
                    PromptMessage(role="user",
                                  content=TextContent(text=f"请审核这段 Python 代码:\n{code}"))
                ]
                return PromptResult(description="代码审查 prompt", messages=messages)
            elif name == "translate":
                text = arguments.get("text") if arguments else None
                language = arguments.get("language") if arguments else None
                if not text or not language:
                     raise HTTPException(status_code=422, detail="缺少 text 或 language 参数") #Invalid params -32602

                messages = [
                    PromptMessage(role="user",
                                  content=TextContent(text=f"请将这段文字翻译成{language}:\n{text}"))
                ]
                return PromptResult(description="翻译 prompt", messages=messages)

            else:
                raise HTTPException(status_code=404, detail="Prompt 未找到")
        self.include_router(router)