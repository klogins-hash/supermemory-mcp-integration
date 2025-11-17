#!/usr/bin/env python3
"""
Supermemory MCP Server
Provides tools to search and manage Supermemory memories via MCP protocol
"""

import asyncio
import json
import os
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from supermemory import Supermemory

# Initialize Supermemory client
SUPERMEMORY_API_KEY = os.getenv("SUPERMEMORY_API_KEY")

if not SUPERMEMORY_API_KEY:
    raise ValueError("SUPERMEMORY_API_KEY environment variable is required")

client = Supermemory(
    api_key=SUPERMEMORY_API_KEY,
    base_url="https://api.supermemory.ai/"
)

# Create MCP server
app = Server("supermemory")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Supermemory tools."""
    return [
        Tool(
            name="search_memories",
            description="Search across all Supermemory memories using semantic search. Returns relevant documents and chunks based on the query.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant memories"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="add_memory",
            description="Add a new memory/document to Supermemory. This can be text content, notes, or any information you want to store.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content to store as a memory"
                    },
                    "title": {
                        "type": "string",
                        "description": "Optional title for the memory"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional metadata for the memory (key-value pairs)"
                    }
                },
                "required": ["content"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""

    if name == "search_memories":
        query = arguments.get("query")
        limit = arguments.get("limit", 5)

        try:
            response = client.search.execute(q=query)

            if not response.results:
                return [TextContent(
                    type="text",
                    text="No memories found matching your query."
                )]

            # Format results
            results = []
            for i, result in enumerate(response.results[:limit], 1):
                title = getattr(result, 'title', 'Untitled')
                score = getattr(result, 'score', 0)
                summary = getattr(result, 'summary', None)

                result_text = f"\n{'='*80}\nResult {i}: {title}\nRelevance Score: {score:.4f}\n"

                if summary:
                    result_text += f"\nSummary: {summary}\n"

                # Get chunks
                chunks = getattr(result, 'chunks', None)
                if chunks:
                    result_text += f"\nContent ({len(chunks)} chunks):\n"
                    for j, chunk in enumerate(chunks[:3], 1):  # First 3 chunks
                        if hasattr(chunk, 'content') and chunk.content:
                            result_text += f"\n--- Chunk {j} ---\n{chunk.content}\n"

                # Get metadata
                metadata = getattr(result, 'metadata', None)
                if metadata:
                    result_text += f"\nMetadata: {metadata}\n"

                results.append(result_text)

            full_response = f"Found {len(response.results)} memories (showing top {min(limit, len(response.results))}):\n" + "\n".join(results)

            return [TextContent(type="text", text=full_response)]

        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error searching memories: {str(e)}"
            )]

    elif name == "add_memory":
        content = arguments.get("content")
        title = arguments.get("title")
        metadata = arguments.get("metadata", {})

        try:
            # Prepare the document data
            document_data = {"content": content}

            if title:
                document_data["title"] = title

            if metadata:
                document_data["metadata"] = metadata

            # Add the memory
            response = client.documents.add(**document_data)

            return [TextContent(
                type="text",
                text=f"Successfully added memory!\nDocument ID: {getattr(response, 'id', 'Unknown')}\nStatus: {getattr(response, 'status', 'Unknown')}"
            )]

        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error adding memory: {str(e)}"
            )]

    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
