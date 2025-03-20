# import asyncio
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
# from pydantic import AnyUrl
import mcp.server.stdio
import os
from dotenv import load_dotenv
load_dotenv()  # 从.env文件加载环境变量


server = Server("jmobile-location-mcp-server")

JUHE_MOBILE_LOCATION_API_BASE = "http://apis.juhe.cn/mobile/"
JUHE_MOBILE_LOCATION_API_KEY = os.environ.get("JUHE_MOBILE_LOCATION_API_KEY")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="get_mobile_location",
            description="根据手机号码查询手机号码归属地、所属号段、手机卡类型、运营商等信息。",
            inputSchema={
                "type": "object",
                "properties": {
                    "phone": {"type": "string", "description": "手机号码"},
                },
                "required": ["phone"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if name == "get_mobile_location":
        phone = arguments.get("phone") if arguments else None
        if not phone:
            raise ValueError("Missing name or phone")
        return await get_mobile_location(phone)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def get_mobile_location(phone: str = "") -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    根据手机号码查询手机号码归属地、所属号段、手机卡类型、运营商等信息。
    """
    url = f"{JUHE_MOBILE_LOCATION_API_BASE}/get"
    params = {
        "phone": phone,
        "key": JUHE_MOBILE_LOCATION_API_KEY
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        if data["error_code"] == 0:
            news_list = data["result"]
            return [
                types.TextContent(
                    type="text",
                    text=f"{news_list}"
                )
            ]
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"Error: {data['reason']}"
                )
            ]

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="jmobile-location-mcp-server",
                server_version="0.1.1",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )