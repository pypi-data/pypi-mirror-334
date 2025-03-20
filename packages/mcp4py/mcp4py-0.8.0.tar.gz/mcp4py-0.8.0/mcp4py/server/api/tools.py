from fastapi import FastAPI, APIRouter, Request, HTTPException
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

# 定义数据模型，对应文档中的数据类型

class InputSchema(BaseModel):
    type: str = "object" # 默认值
    properties: Dict[str, Dict[str, str]] # 键为属性名，值为属性描述 (type, description)
    required: List[str] # 必须的属性名

class Tool(BaseModel):
    name: str
    description: str
    inputSchema: InputSchema

class ToolResultContent(BaseModel):
    type: str
    text: Optional[str] = None # 文本内容
    data: Optional[str] = None # base64 编码数据
    mimeType: Optional[str] = None # MIME 类型
    resource: Optional[Dict[str,Any]] = None # 内嵌资源

class ToolResult(BaseModel):
    content: List[ToolResultContent]
    isError: bool = False

class ToolsListResponse(BaseModel):
    tools: List[Tool]
    nextCursor: Optional[str] = None

class ToolsCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]

class Tools(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tools_list: List[Tool] = []  # 存储tools列表
        self.setup_routes_tools()
        self.capabilities = {
          "capabilities": {
            "tools": {
              "listChanged": True #  如果服务器在可用工具列表更改时发出通知，设置为True
            }
          }
        }

    def setup_routes_tools(self):
        router = APIRouter(prefix="", tags=["tools"])

        @router.get("/capabilities")
        async def get_capabilities():
            """
            返回服务器的功能声明。
            """
            return self.capabilities

        @router.post("/tools/list")
        async def list_tools(cursor: Optional[str] = None) -> ToolsListResponse:
            """
            列出可用的工具。支持分页。
            """
            # 在实际应用中，您可能需要根据 cursor 参数实现分页逻辑。
            # 这里仅返回所有工具。
            return ToolsListResponse(tools=self.tools_list)

        @router.post("/tools/call")
        async def call_tool(request: ToolsCallRequest) -> ToolResult:
            """
            调用一个工具。
            """
            tool_name = request.name
            arguments = request.arguments

            # 查找对应的工具
            tool = next((t for t in self.tools_list if t.name == tool_name), None)

            if not tool:
                raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")

            # 在实际应用中，您需要根据 tool 的 inputSchema 验证 arguments
            # 并调用相应的函数来执行工具。
            try:
                result = await self.execute_tool(tool, arguments)  # 假设有这个执行工具的函数
                return result
            except Exception as e:
                return ToolResult(content=[ToolResultContent(type="text", text=f"Tool execution failed: {str(e)}")], isError=True)

        self.include_router(router)


    async def execute_tool(self, tool: Tool, arguments: Dict[str, Any]) -> ToolResult:
        """
        执行工具的示例函数。 需要根据工具的实际逻辑进行实现。
        注意：应该在此处处理参数验证、错误处理和安全性。
        """
        # 示例：假设有一个名为 "get_weather" 的工具，它接受一个 "location" 参数。
        if tool.name == "get_weather":
            location = arguments.get("location")
            if not location:
                return ToolResult(content=[ToolResultContent(type="text", text="Missing location parameter")], isError=True)
            # 模拟获取天气数据
            weather_data = f"Current weather in {location}: Sunny, 25°C"
            return ToolResult(content=[ToolResultContent(type="text", text=weather_data)])
        else:
            return ToolResult(content=[ToolResultContent(type="text", text="Tool execution not implemented")], isError=True)


    def add_tool(self, tool: Tool):
        """
        添加工具到tools列表中
        """
        self.tools_list.append(tool)

# 示例用法：
if __name__ == "__main__":
    import uvicorn

    # 创建 Tools 实例
    tools_app = Tools(title="My Tools API")

    # 添加一个示例工具
    weather_tool = Tool(
        name="get_weather",
        description="Get current weather information for a location",
        inputSchema=InputSchema(
            properties={
                "location": {"type": "string", "description": "City name or zip code"}
            },
            required=["location"],
        ),
    )
    tools_app.add_tool(weather_tool)

    # 运行 FastAPI 应用
    uvicorn.run(tools_app, host="0.0.0.0", port=8000)