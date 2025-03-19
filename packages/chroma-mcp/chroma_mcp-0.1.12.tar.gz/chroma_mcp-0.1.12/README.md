<p align="center">
  <a href="https://trychroma.com"><img src="https://user-images.githubusercontent.com/891664/227103090-6624bf7d-9524-4e05-9d2c-c28d5d451481.png" alt="Chroma logo"></a>
</p>

<p align="center">
    <b>Chroma - the open-source embedding database</b>. <br />
    The fastest way to build Python or JavaScript LLM apps with memory!
</p>

<p align="center">
  <a href="https://discord.gg/MMeYNTmh3x" target="_blank">
      <img src="https://img.shields.io/discord/1073293645303795742?cacheSeconds=3600" alt="Discord">
  </a> |
  <a href="https://github.com/chroma-core/chroma/blob/master/LICENSE" target="_blank">
      <img src="https://img.shields.io/static/v1?label=license&message=Apache 2.0&color=white" alt="License">
  </a> |
  <a href="https://docs.trychroma.com/" target="_blank">
      Docs
  </a> |
  <a href="https://www.trychroma.com/" target="_blank">
      Homepage
  </a>
</p>

# Chroma MCP Server

[The Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) is an open protocol designed for effortless integration between LLM applications and external data sources or tools, offering a standardized framework to seamlessly provide LLMs with the context they require.

This server provides data retrieval capabilities powered by Chroma, enabling AI models to create collections over generated data and user inputs, and retrieve that data using vector search, full text search, metadata filtering, and more.

## Features

- **Flexible Client Types**
  - Ephemeral (in-memory) for testing and development
  - Persistent for file-based storage
  - HTTP client for self-hosted Chroma instances
  - Cloud client for Chroma Cloud integration (automatically connects to api.trychroma.com)

- **Collection Management**
  - Create, modify, and delete collections
  - List all collections with pagination support
  - Get collection information and statistics
  - Configure HNSW parameters for optimized vector search

- **Document Operations**
  - Add documents with optional metadata and custom IDs
  - Query documents using semantic search
  - Advanced filtering using metadata and document content
  - Retrieve documents by IDs or filters
  - Full text search capabilities

### Supported Tools

- `create_collection`
- `peek_collection`
- `list_collections`
- `get_collection_info`
- `get_collection_count`
- `modify_collection`
- `delete_collection`
- `add_documents`
- `query_documents`
- `get_documents`

## Usage with Claude Desktop

1. To add an ephemeral client, add the following to your `claude_desktop_config.json` file:

```json
"chroma": {
    "command": "uvx",
    "args": [
        "chroma-mcp"
    ]
}
```

2. To add a persistent client, add the following to your `claude_desktop_config.json` file:

```json
"chroma": {
    "command": "uvx",
    "args": [
        "chroma-mcp",
        "--client-type",
        "persistent",
        "--data-dir",
        "/full/path/to/your/data/directory"
    ]
}
```

This will create a persistent client that will use the data directory specified.

3. To connect to Chroma Cloud, add the following to your `claude_desktop_config.json` file:

```json
"chroma": {
    "command": "uvx",
    "args": [
        "chroma-mcp",
        "--client-type",
        "cloud",
        "--tenant",
        "your-tenant-id",
        "--database",
        "your-database-name",
        "--api-key",
        "your-api-key"
    ]
}
```

This will create a cloud client that automatically connects to api.trychroma.com using SSL.

4. To connect to a [self-hosted Chroma instance on your own cloud provider](https://docs.trychroma.com/
production/deployment), add the following to your `claude_desktop_config.json` file:

```json
"chroma": {
    "command": "uvx",
    "args": [
      "chroma-mcp", 
      "--client-type", 
      "http", 
      "--host", 
      "your-host", 
      "--port", 
      "your-port", 
      "--custom-auth-credentials",
      "your-custom-auth-credentials",
      "--ssl",
      "true"
    ]
}
```

This will create an HTTP client that connects to your self-hosted Chroma instance.

### Using Environment Variables

You can also use environment variables to configure the client:

```bash
# Common variables
export CHROMA_CLIENT_TYPE="http"  # or "cloud", "persistent", "ephemeral"

# For persistent client
export CHROMA_DATA_DIR="/full/path/to/your/data/directory"

# For cloud client (Chroma Cloud)
export CHROMA_TENANT="your-tenant-id"
export CHROMA_DATABASE="your-database-name"
export CHROMA_API_KEY="your-api-key"

# For HTTP client (self-hosted)
export CHROMA_HOST="your-host"
export CHROMA_PORT="your-port"
export CHROMA_CUSTOM_AUTH_CREDENTIALS="your-custom-auth-credentials"
export CHROMA_SSL="true"
```

