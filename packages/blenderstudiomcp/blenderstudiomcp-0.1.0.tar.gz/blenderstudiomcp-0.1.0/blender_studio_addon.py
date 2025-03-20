import bpy
import json
import threading
import socket
import time
from bpy.props import StringProperty, IntProperty

bl_info = {
    "name": "BlenderStudioMCP",
    "author": "BlenderStudioMCP",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > BlenderStudioMCP",
    "description": "Connect Blender to Claude via MCP for Blender Studio",
    "category": "Interface",
}

class BlenderStudioMCPServer:
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.running = False
        self.socket = None
        self.client = None
        self.server_thread = None

    def start(self):
        self.running = True
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        print(f"BlenderStudioMCP server started on {self.host}:{self.port}")

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()
        if self.client:
            self.client.close()
        print("BlenderStudioMCP server stopped")

    def execute_command(self, command):
        """Execute commands received from the MCP server"""
        if not isinstance(command, dict):
            return {"status": "error", "message": "Invalid command format"}

        cmd_type = command.get("type")
        if cmd_type == "check_version":
            return {
                "status": "success",
                "data": {
                    "blender_version": bpy.app.version_string,
                    "blender_build_date": bpy.app.build_date.decode('utf-8'),
                    "python_version": bpy.app.version_string
                }
            }
        else:
            return {"status": "error", "message": f"Unknown command type: {cmd_type}"}

    def _run_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.socket.settimeout(1.0)  # Add a timeout for accept

            while self.running:
                try:
                    self.client, address = self.socket.accept()
                    print(f"Connected to client: {address}")

                    while self.running:
                        try:
                            # Set a timeout for receiving data
                            self.client.settimeout(15.0)
                            data = self.client.recv(4096)

                            if not data:
                                print("Empty data received, client may have disconnected")
                                break

                            try:
                                print(f"Received data: {data.decode('utf-8')}")
                                command = json.loads(data.decode('utf-8'))
                                response = self.execute_command(command)
                                print(f"Sending response: {json.dumps(response)[:100]}...")  # Truncate long responses in log
                                self.client.sendall(json.dumps(response).encode('utf-8'))
                            except json.JSONDecodeError:
                                print(f"Invalid JSON received: {data.decode('utf-8')}")
                                self.client.sendall(json.dumps({
                                    "status": "error",
                                    "message": "Invalid JSON format"
                                }).encode('utf-8'))
                            except Exception as e:
                                print(f"Error executing command: {str(e)}")
                                import traceback
                                traceback.print_exc()
                                self.client.sendall(json.dumps({
                                    "status": "error",
                                    "message": str(e)
                                }).encode('utf-8'))

                        except socket.timeout:
                            print("Socket timeout while waiting for data")
                            continue
                        except Exception as e:
                            print(f"Error receiving data: {str(e)}")
                            break

                except socket.timeout:
                    continue  # No connection attempts
                except Exception as e:
                    print(f"Error accepting connection: {str(e)}")
                    time.sleep(1)  # Avoid tight loop on error

        except Exception as e:
            print(f"Server error: {str(e)}")
        finally:
            if self.socket:
                self.socket.close()

class BlenderStudioMCPPanel(bpy.types.Panel):
    bl_label = "BlenderStudioMCP"
    bl_idname = "VIEW3D_PT_blenderstudiomcp"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BlenderStudioMCP'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "blenderstudiomcp_port")
        
        if not hasattr(bpy.types.Scene, "blenderstudiomcp_server"):
            layout.operator("blenderstudiomcp.start_server")
        else:
            layout.operator("blenderstudiomcp.stop_server")

class BlenderStudioMCPStart(bpy.types.Operator):
    bl_idname = "blenderstudiomcp.start_server"
    bl_label = "Start Server"
    bl_description = "Start the BlenderStudioMCP server"

    def execute(self, context):
        if hasattr(bpy.types.Scene, "blenderstudiomcp_server"):
            self.report({'WARNING'}, "Server is already running")
            return {'CANCELLED'}

        port = context.scene.blenderstudiomcp_port
        server = BlenderStudioMCPServer(port=port)
        server.start()
        bpy.types.Scene.blenderstudiomcp_server = server
        return {'FINISHED'}

class BlenderStudioMCPStop(bpy.types.Operator):
    bl_idname = "blenderstudiomcp.stop_server"
    bl_label = "Stop Server"
    bl_description = "Stop the BlenderStudioMCP server"

    def execute(self, context):
        if not hasattr(bpy.types.Scene, "blenderstudiomcp_server"):
            self.report({'WARNING'}, "Server is not running")
            return {'CANCELLED'}

        server = bpy.types.Scene.blenderstudiomcp_server
        server.stop()
        del bpy.types.Scene.blenderstudiomcp_server
        return {'FINISHED'}

def register():
    bpy.types.Scene.blenderstudiomcp_port = IntProperty(
        name="Port",
        description="Port for the BlenderStudioMCP server",
        default=9876,
        min=1024,
        max=65535
    )
    
    bpy.utils.register_class(BlenderStudioMCPPanel)
    bpy.utils.register_class(BlenderStudioMCPStart)
    bpy.utils.register_class(BlenderStudioMCPStop)

def unregister():
    if hasattr(bpy.types.Scene, "blenderstudiomcp_server"):
        bpy.types.Scene.blenderstudiomcp_server.stop()
        del bpy.types.Scene.blenderstudiomcp_server

    del bpy.types.Scene.blenderstudiomcp_port
    
    bpy.utils.unregister_class(BlenderStudioMCPPanel)
    bpy.utils.unregister_class(BlenderStudioMCPStart)
    bpy.utils.unregister_class(BlenderStudioMCPStop)

if __name__ == "__main__":
    register() 