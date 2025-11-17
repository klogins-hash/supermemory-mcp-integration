# Supermemory MCP Integration for Claude

This project provides a custom MCP (Model Context Protocol) server that integrates Supermemory with Claude Desktop, allowing you to search and manage your memories directly from Claude conversations.

## ⚠️ Official Supermemory MCP Available

Supermemory now offers an official MCP server with SSE transport. You can use either:

### Option 1: Official Supermemory MCP (Recommended)
Get the latest version from [app.supermemory.ai](https://app.supermemory.ai):
1. Sign in to your Supermemory account
2. Navigate to "Connect to your AI" → Select Claude
3. Get your unique MCP URL: `https://mcp.supermemory.ai/[YOUR_UNIQUE_ID]/sse`
4. Install with: `npx install-mcp [YOUR_URL] --client claude`

**Benefits**: Always up-to-date, officially maintained, SSE transport

### Option 2: This Custom Implementation
Use this repository for:
- Custom modifications and extensions
- Learning how MCP servers work
- Offline/local-first operation
- Integration with other MCP-compatible tools

**Note**: Both implementations work with Supermemory's v3 API. This custom version uses stdio transport instead of SSE.

## Features

- **Search Memories**: Semantic search across all your Supermemory documents
- **Add Memories**: Store new information and conversations in Supermemory
- **Chat with Your Memories**: Ask Claude questions and it will search your Supermemory database for relevant context

## Prerequisites

- Python 3.10 or higher
- Claude Desktop app
- Supermemory account and API key

## Setup Instructions

### 1. Install Dependencies

```bash
cd /Users/franksimpson/CascadeProjects/supermemory-claude-integration
source venv/bin/activate  # If venv already exists
# OR create a new venv:
# python3 -m venv venv
# source venv/bin/activate

pip install -r requirements.txt
```

### 2. Set Up API Key

Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

Then edit `.env` and add your Supermemory API key:

```
SUPERMEMORY_API_KEY=your_actual_api_key_here
```

Get your API key from: https://console.supermemory.ai

### 3. Configure Claude Desktop

Run the setup script to automatically configure Claude Desktop:

```bash
source venv/bin/activate
SUPERMEMORY_API_KEY=your_api_key_here python setup_claude_config.py
```

Or manually add the configuration to your Claude Desktop config file:

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "supermemory": {
      "command": "/path/to/supermemory-claude-integration/venv/bin/python",
      "args": [
        "/path/to/supermemory-claude-integration/supermemory_mcp_server.py"
      ],
      "env": {
        "SUPERMEMORY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Note**: Replace `/path/to/supermemory-claude-integration/` with your actual project path. If you already have other MCP servers configured, just add the "supermemory" entry to the existing "mcpServers" object.

### 3. Restart Claude Desktop

After updating the config file, completely quit and restart Claude Desktop for the changes to take effect.

### 4. Verify the Integration

In Claude Desktop, you should now see the Supermemory tools available. Try asking:

- "Search my memories for information about Aura"
- "What do you know about my projects?"
- "Search for information about AI companions in my memories"

## Available Tools

### 1. search_memories

Search across all your Supermemory memories using semantic search.

**Parameters**:
- `query` (required): The search query
- `limit` (optional): Maximum number of results (default: 5)

**Example**:
```
Search my memories for: "AI agent architecture"
```

### 2. add_memory

Add a new memory/document to Supermemory.

**Parameters**:
- `content` (required): The content to store
- `title` (optional): Title for the memory
- `metadata` (optional): Additional metadata as key-value pairs

**Example**:
```
Add this to my memories: "Today I learned about MCP servers and how they integrate with Claude"
```

## Testing

### Test the Search Functionality

Run the test script to verify your Supermemory connection:

```bash
source venv/bin/activate
python test_search.py
```

This will search your existing memories and display the results.

### Test the MCP Server Directly

You can test the MCP server in isolation:

```bash
source venv/bin/activate
python supermemory_mcp_server.py
```

The server will start and wait for MCP protocol messages on stdin.

## Usage Examples

Once configured in Claude Desktop, you can have conversations like:

**Example 1: Searching memories**
```
You: What projects have I worked on related to AI agents?
Claude: Let me search your memories... [uses search_memories tool]
```

**Example 2: Adding memories**
```
You: Remember that I prefer to use Python for backend development
Claude: [uses add_memory tool to store this preference]
```

**Example 3: Context-aware conversations**
```
You: Based on what you know about my Aura project, what should I focus on next?
Claude: [searches memories for Aura project details and provides recommendations]
```

## Uploading Claude Conversations to Supermemory

To automatically upload Claude conversations to Supermemory, you can:

1. **Manual Upload**: Copy important conversation snippets and use the `add_memory` tool
2. **Batch Upload**: Save conversations as text files and upload them using the Supermemory API

## Project Structure

```
supermemory-claude-integration/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── supermemory_mcp_server.py   # MCP server implementation
├── test_search.py              # Test script for searching memories
└── venv/                       # Python virtual environment
```

## Troubleshooting

### MCP Server not showing in Claude

1. Check that the config file path is correct: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Verify the Python path in the config points to your venv's Python
3. Make sure Claude Desktop is completely restarted (quit and reopen)
4. Check Claude Desktop logs for any error messages

### Search not returning results

1. Verify your API key is correct
2. Check that you have memories in your Supermemory account at https://console.supermemory.ai
3. Try running `test_search.py` to verify the connection works

### API Errors

1. Ensure your Supermemory API key is valid
2. Check your internet connection
3. Verify the API endpoint is accessible

## API Key Security

**Important**: The API key is currently hardcoded in this project. For production use, you should:

1. Use environment variables
2. Store the key in a secure location
3. Never commit API keys to version control

To use environment variables:

```bash
export SUPERMEMORY_API_KEY="your_key_here"
```

Then update the MCP server config to not include the key in the JSON (it will use the environment variable).

## Next Steps

- Add conversation export functionality
- Implement automatic conversation tracking
- Add support for filtering by tags/metadata
- Create a UI for managing memories

## Resources

- [Supermemory Documentation](https://supermemory.ai/docs)
- [MCP Protocol Documentation](https://modelcontextprotocol.io)
- [Supermemory Console](https://console.supermemory.ai)

## License

MIT
