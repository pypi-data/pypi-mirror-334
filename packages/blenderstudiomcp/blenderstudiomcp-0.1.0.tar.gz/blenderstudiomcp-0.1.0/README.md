# BlenderStudioMCP MCP Server

A Model Context Protocol (MCP) server for Blender Studio integration.

## Components

### Blender Addon

The BlenderStudioMCP system consists of two parts:
1. A Blender addon (`blender_studio_addon.py`) that runs inside Blender
2. An MCP server that communicates with Claude and the Blender addon

### Resources

The server is ready to be extended with custom resources.

### Prompts

The server is ready to be extended with custom prompts.

### Tools

The server provides the following tools:
- `check_blender_version`: Get information about the current Blender installation

## Installation

### 1. Install the Blender Addon

1. Open Blender
2. Go to Edit > Preferences > Add-ons
3. Click "Install..."
4. Navigate to and select `blender_studio_addon.py`
5. Enable the addon by checking the box next to "Interface: BlenderStudioMCP"
6. The addon will appear in the 3D Viewport's sidebar (press N to show)
7. In the BlenderStudioMCP panel, click "Start Server"

### 2. Configure Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "BlenderStudioMCP": {
      "command": "uv",
      "args": [
        "--directory",
        "E:\CursorAI\BlenderStudioMCP",
        "run",
        "blenderstudiomcp"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  ```
  "mcpServers": {
    "BlenderStudioMCP": {
      "command": "uvx",
      "args": [
        "blenderstudiomcp"
      ]
    }
  }
  ```
</details>

## Usage

1. Start Blender
2. Enable the BlenderStudioMCP addon in the 3D Viewport sidebar (N key)
3. Click "Start Server" in the BlenderStudioMCP panel
4. Start Claude Desktop
5. The `check_blender_version` tool will be available to use in Claude

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
npx @modelcontextprotocol/inspector uv --directory E:\CursorAI\BlenderStudioMCP run blenderstudiomcp
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

### Testing the Blender Connection

1. Start Blender and enable the addon
2. Click "Start Server" in the BlenderStudioMCP panel
3. Use the MCP Inspector to test the `check_blender_version` tool
4. The response should include Blender version, build date, and Python version