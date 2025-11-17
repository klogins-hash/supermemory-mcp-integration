#!/usr/bin/env python3
"""
Helper script to add Supermemory MCP server to Claude Desktop config
"""

import json
import os
import shutil
from pathlib import Path

# Claude Desktop config location
CLAUDE_CONFIG_PATH = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"

# Project paths
PROJECT_DIR = Path(__file__).parent
VENV_PYTHON = PROJECT_DIR / "venv/bin/python"
SERVER_SCRIPT = PROJECT_DIR / "supermemory_mcp_server.py"

# Get API key from environment or prompt user
SUPERMEMORY_API_KEY = os.getenv("SUPERMEMORY_API_KEY")

if not SUPERMEMORY_API_KEY:
    print("⚠️  SUPERMEMORY_API_KEY environment variable not found.")
    SUPERMEMORY_API_KEY = input("Please enter your Supermemory API key: ").strip()
    if not SUPERMEMORY_API_KEY:
        print("❌ Error: API key is required")
        exit(1)

# MCP server configuration
SUPERMEMORY_CONFIG = {
    "supermemory": {
        "command": str(VENV_PYTHON),
        "args": [str(SERVER_SCRIPT)],
        "env": {
            "SUPERMEMORY_API_KEY": SUPERMEMORY_API_KEY
        }
    }
}


def main():
    """Add Supermemory MCP server configuration to Claude Desktop."""

    print("🔧 Setting up Supermemory MCP Server for Claude Desktop\n")

    # Check if venv exists
    if not VENV_PYTHON.exists():
        print(f"❌ Error: Virtual environment not found at {VENV_PYTHON}")
        print("   Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt")
        return 1

    # Check if server script exists
    if not SERVER_SCRIPT.exists():
        print(f"❌ Error: Server script not found at {SERVER_SCRIPT}")
        return 1

    # Create backup of existing config
    if CLAUDE_CONFIG_PATH.exists():
        backup_path = CLAUDE_CONFIG_PATH.with_suffix('.json.backup')
        shutil.copy2(CLAUDE_CONFIG_PATH, backup_path)
        print(f"✅ Created backup at {backup_path}")

    # Read existing config or create new one
    if CLAUDE_CONFIG_PATH.exists():
        with open(CLAUDE_CONFIG_PATH, 'r') as f:
            config = json.load(f)
        print(f"✅ Loaded existing config from {CLAUDE_CONFIG_PATH}")
    else:
        config = {}
        print(f"📝 Creating new config file")
        # Create directory if it doesn't exist
        CLAUDE_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Ensure mcpServers section exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Add or update Supermemory server
    if "supermemory" in config["mcpServers"]:
        print("\n⚠️  Supermemory server already exists in config. Updating...")

    config["mcpServers"].update(SUPERMEMORY_CONFIG)

    # Write updated config
    with open(CLAUDE_CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\n✅ Successfully updated Claude Desktop config!")
    print(f"   Config location: {CLAUDE_CONFIG_PATH}")
    print(f"\n📋 Configuration added:")
    print(json.dumps(SUPERMEMORY_CONFIG, indent=2))

    print("\n" + "="*80)
    print("🚀 Next Steps:")
    print("="*80)
    print("1. Completely quit Claude Desktop (Cmd+Q)")
    print("2. Restart Claude Desktop")
    print("3. Look for the Supermemory tools in Claude")
    print("\n💡 Try asking Claude:")
    print('   - "Search my memories for Aura"')
    print('   - "What do you know about my projects?"')
    print('   - "Add to my memories: I prefer Python for backend development"')
    print("="*80)

    return 0


if __name__ == "__main__":
    exit(main())
