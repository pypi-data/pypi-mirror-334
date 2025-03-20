import asyncio
import socket
import json

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# Initialize the server
server = Server("BlenderStudioMCP")

class BlenderConnection:
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.socket = None

    async def connect(self):
        try:
            # Create a new socket connection for each request
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)  # 5 second timeout
            self.socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Failed to connect to Blender: {str(e)}")
            return False

    async def send_command(self, command):
        try:
            if not await self.connect():
                return {"status": "error", "message": "Could not connect to Blender"}

            # Send command
            self.socket.sendall(json.dumps(command).encode('utf-8'))
            
            # Receive response
            response = self.socket.recv(4096)
            return json.loads(response.decode('utf-8'))
        except Exception as e:
            return {"status": "error", "message": f"Error communicating with Blender: {str(e)}"}
        finally:
            if self.socket:
                self.socket.close()

# Create a global connection instance
blender = BlenderConnection()

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available resources.
    """
    return []

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    """
    return []

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    """
    return [
        types.Tool(
            name="check_blender_version",
            description="Get the current Blender version information",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    """
    if name != "check_blender_version":
        raise ValueError(f"Unknown tool: {name}")

    response = await blender.send_command({"type": "check_version"})
    
    if response["status"] == "error":
        return [
            types.TextContent(
                type="text",
                text=f"Error checking Blender version: {response['message']}"
            )
        ]

    version_info = response["data"]
    return [
        types.TextContent(
            type="text",
            text=f"Blender Version: {version_info['blender_version']}\n"
                 f"Build Date: {version_info['blender_build_date']}\n"
                 f"Python Version: {version_info['python_version']}"
        )
    ]

async def main():
    """Main entry point for the MCP server."""
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="BlenderStudioMCP",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )