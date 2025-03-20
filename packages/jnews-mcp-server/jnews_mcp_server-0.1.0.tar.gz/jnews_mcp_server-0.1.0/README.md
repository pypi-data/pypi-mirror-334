# jnews-mcp-server MCP server

获取今日热点新闻头条信息

## Components

### Tools

服务器实现了两个工具:
- get_news_list: 根据新闻类型获取今日热点新闻头条
  - 需要传入 "type"（新闻类型）作为选填的字符串参数。
- get_news_content: 根据新闻类型获取今日热点新闻头条
  - 需要传入 "uniquekey"（新闻id）作为必须的字符串参数。

## Configuration

[TODO: Add configuration details specific to your implementation]
### Environment Variables
- `JUHE_NEWS_API_KEY`: 聚合数据的新闻头条API密钥。获取：[https://www.juhe.cn/docs/api/id/235](https://www.juhe.cn/docs/api/id/235)
```
JUHE_NEWS_API_KEY=your_api_key
```

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>

  ```
  "mcpServers": {
    "jnews-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/juheapi-mcp-server/jnews-mcp-server",
        "run",
        "jnews-mcp-server"
      ],
      "env": {
        "JUHE_NEWS_API_KEY": "your_api_key"
      }
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>

  ```
  "mcpServers": {
    "jnews-mcp-server": {
      "command": "uvx",
      "args": [
        "jnews-mcp-server"
      ],
      "env": {
        "JUHE_NEWS_API_KEY": "your_api_key"
      }
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/juheapi-mcp-server/jnews-mcp-server run jnews-mcp-server
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.