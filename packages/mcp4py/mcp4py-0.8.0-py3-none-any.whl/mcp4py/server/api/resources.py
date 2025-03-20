from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Union
import base64


class Resource(BaseModel):
    uri: str
    name: str
    description: Optional[str] = None
    mimeType: Optional[str] = None
    size: Optional[int] = None  # in bytes


class TextContent(BaseModel):
    uri: str
    mimeType: str
    text: str


class BinaryContent(BaseModel):
    uri: str
    mimeType: str
    blob: str  # Base64 encoded data


ResourceContent = Union[TextContent, BinaryContent]


class ResourceTemplate(BaseModel):
    uriTemplate: str
    name: str
    description: Optional[str] = None
    mimeType: str


class Resources(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_routes_resources()
        self.resources = self.initialize_resources()  # 模拟资源存储
        self.resource_templates = self.initialize_resource_templates()
        self.subscriptions = {}  # uri: list of clients, for notification

    def initialize_resources(self):
        # 模拟一些资源数据
        return {
            "file:///project/src/main.rs": Resource(
                uri="file:///project/src/main.rs",
                name="main.rs",
                description="Primary application entry point",
                mimeType="text/x-rust",
            ),
            "file:///project/data/config.json": Resource(
                uri="file:///project/data/config.json",
                name="config.json",
                description="Application configuration file",
                mimeType="application/json",
            ),
            "https://www.example.com/logo.png": Resource(
                uri="https://www.example.com/logo.png",
                name="logo.png",
                description="Application logo",
                mimeType="image/png",
            )
        }

    def initialize_resource_templates(self):
        return [
            ResourceTemplate(
                uriTemplate="file:///{path}",
                name="Project Files",
                description="Access files in the project directory",
                mimeType="application/octet-stream",
            )
        ]

    def setup_routes_resources(self):
        router = APIRouter(prefix="/resources", tags=["resources"],
                           responses={404: {"description": "Resource not found"}})

        @router.post("/list")
        async def list_resources(cursor: Optional[str] = None):  # 模拟分页
            # 在真实场景中，根据 cursor 进行分页处理
            resource_list = list(self.resources.values())
            next_cursor = None  # 模拟没有下一页
            return {"resources": resource_list, "nextCursor": next_cursor}

        @router.post("/read")
        async def read_resource(uri: str):
            resource = self.resources.get(uri)
            if not resource:
                raise HTTPException(status_code=404,
                                    detail={"code": -32002, "message": "Resource not found", "data": {"uri": uri}})

            # 模拟返回资源内容 (根据 MIME 类型返回 text 或 blob)
            if resource.mimeType.startswith("text/"):
                # 假设文件内容存在（实际应用中从文件系统或数据库读取）
                text_content = f"This is the text content of {resource.name}."
                return {"contents": [TextContent(uri=uri, mimeType=resource.mimeType, text=text_content)]}
            elif resource.mimeType.startswith("image/"):
                # 模拟二进制数据 (base64 编码)
                binary_data = base64.b64encode(b"dummy image data").decode("utf-8")  # 替换为实际数据
                return {"contents": [BinaryContent(uri=uri, mimeType=resource.mimeType, blob=binary_data)]}
            else:
                return {"contents": [
                    TextContent(uri=uri, mimeType=resource.mimeType, text=f"Unknown content type for {resource.name}")]}
            # raise HTTPException(status_code=500, detail="Content type not supported.")

        @router.post("/templates/list")
        async def list_resource_templates():
            return {"resourceTemplates": self.resource_templates}

        @router.post("/subscribe")
        async def subscribe_resource(uri: str):
            # 模拟订阅功能
            if uri not in self.resources:
                raise HTTPException(status_code=404,
                                    detail={"code": -32002, "message": "Resource not found", "data": {"uri": uri}})

            # TODO: 在实际应用中应该使用 WebSocket 连接来实现实时通知

            # 模拟成功订阅
            return {"message": f"Subscribed to resource: {uri}"}

        self.include_router(router)