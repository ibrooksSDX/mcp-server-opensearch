# mcp-server-opensearch: An OpenSearch MCP Server
[![smithery badge](https://smithery.ai/badge/@ibrooksSDX/mcp-server-opensearch)](https://smithery.ai/server/@ibrooksSDX/mcp-server-opensearch)

> The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) is an open protocol that enables seamless integration between LLM applications and external data sources and tools. Whether you’re building an AI-powered IDE, enhancing a chat interface, or creating custom AI workflows, MCP provides a standardized way to connect LLMs with the context they need.

This repository is an example of how to create a MCP server for [OpenSearch](https://opensearch.org/), a distributed search and analytics engine.

# Under Contruction 

![image1](./images/claude1.png)
![image2](./images/mcpDev1.png)


## Current Blocker - Async Client from OpenSearch isn't installing

[Open Search Async Client Docs](https://github.com/opensearch-project/opensearch-py/blob/main/guides/async.m) 

```shell
pip install opensearch-py[async]
zsh: no matches found: opensearch-py[async]
```

## Overview 

A basic Model Context Protocol server for keeping and retrieving memories in the OpenSearch engine.
It acts as a semantic memory layer on top of the OpenSearch database.

## Components

### Tools

1. `search-openSearch`
   - Store a memory in the OpenSearch database
   - Input:
     - `query` (json): prepared json query message
   - Returns: Confirmation message

## Installation

### Installing via Smithery

To install mcp-server-opensearch for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@ibrooksSDX/mcp-server-opensearch):

```bash
npx -y @smithery/cli install @ibrooksSDX/mcp-server-opensearch --client claude
```

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed to directly run *mcp-server-opensearch*.

```shell
uv run mcp-server-opensearch \
  --opensearch-url "http://localhost:9200" \
  --index-name "my_index" \
```
or 

```shell
uv run fastmcp run demo.py:main
```

## Testing - Local Open Search Client

![image4](./images/osclientTest0.png)

```shell
uv run python src/mcp-server-opensearch/test_opensearch.py
```
## Testing - MCP Server Connection to Open Search Client

![image1](./images/mcpDev0.png)
![image2](./images/mcpDev1.png)

```shell
cd src/mcp-server-opensearch
uv run fastmcp dev demo.py
```

## Usage with Claude Desktop

To use this server with the Claude Desktop app, add the following configuration to the "mcpServers" section of your `claude_desktop_config.json`:

```json
{
  "opensearch": {
    "command": "uvx",
    "args": [
      "mcp-server-opensearch",
      "--opensearch-url",
      "http://localhost:9200",
      "--opensearch-api-key",
      "your_api_key",
      "--index-name",
      "your_index_name"
    ]
  }, "Demo": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "--with",
        "opensearch-py",
        "fastmcp",
        "run",
        "/Users/ibrooks/Documents/GitHub/mcp-server-opensearch/src/mcp-server-opensearch/demo.py"
      ]
    }
}
```

Or use the FastMCP UI to install the server to Claude

```shell
uv run fastmcp install demo.py
```

## Environment Variables

The configuration of the server can be also done using environment variables:

- `OPENSEARCH_HOST`: URL of the OpenSearch server, e.g. `http://localhost`
- `OPENSEARCH_HOSTPORT`: Port of the host of the OpenSearch server `9200`
- `INDEX_NAME`: Name of the index to use
