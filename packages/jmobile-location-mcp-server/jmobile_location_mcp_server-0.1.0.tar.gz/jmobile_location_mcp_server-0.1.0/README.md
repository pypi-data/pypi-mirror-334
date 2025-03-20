# Juhe Mobile Phone Location MCP Server

一个提供手机号码（段）所属归属地查询功能的模型上下文协议（Model Context Protocol）服务器。该服务器使大型语言模型（LLMs）能够获取手机号码段归属地信息，如：省份、城市、运营商。


## Components

### Tools

服务器实现了一个工具:

- get_mobile_phone_location: 根据手机号码查询其所属地信息。
  - 需要传入 "phone"（手机号码）作为必须的字符串参数。
```
async def get_mobile_location(phone: str = "") -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
```


## Install
This server requires Python 3.10 or higher. Install dependencies using uv (recommended) or pip

### Using uv (recommended)
When using [uv](https://docs.astral.sh/uv/) no specific installation is needed. We will use [uvx](https://docs.astral.sh/uv/guides/tools/) to directly run jmobile-location-mcp-server.

```bash
uvx jmobile-location-mcp-server
```

### Using PIP
Alternatively you can install jmobile-location-mcp-server via pip:
```
pip install jmobile-location-mcp-server
```
After installation, you can run it as a script using:
```
python -m jmobile_location_mcp_server
```

### Configuration

#### Environment Variables
`JUHE_MOBILE_LOCATION_API_KEY`: 聚合数据的手机归属地查询API密钥。获取：[https://www.juhe.cn/docs/api/id/11](https://www.juhe.cn/docs/api/id/11)
```
JUHE_MOBILE_LOCATION_API_KEY=your_api_key
```

#### Claude Desktop

- On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Using uvx</summary>

  ```
  "mcpServers": {
    "jmobile-location-mcp-server": {
      "command": "uvx",
      "args": [
        "jmobile-location-mcp-server"
      ],
      "env": {
        "JUHE_MOBILE_LOCATION_API_KEY": "your_api_key"
      }
    }
  }
  ```
</details>

<details>
  <summary>Using pip installation</summary>

  ```
  "mcpServers": {
    "jmobile-location-mcp-server": {
      "command": "python",
      "args": [
        "-m",
        "jmobile_location_mcp_server"
      ],
      "env": {
        "JUHE_MOBILE_LOCATION_API_KEY": "your_api_key"
      }
    }
  }
  ```
</details>

## Debugging
You can use the MCP inspector to debug the server. For uvx installations:

```bash
npx @modelcontextprotocol/inspector uvx jmobile-location-mcp-server 
```

Or if you've installed the package in a specific directory or are developing on it:

```bash
cd path/to/servers/src/jmobile-location-mcp-server
npx @modelcontextprotocol/inspector uv run jmobile-location-mcp-server
```

## Examples of Questions for Cline
1. "查询下这个手机号码的归属地信息 18912341234"