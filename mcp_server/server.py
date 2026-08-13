from mcp.server.fastmcp import FastMCP
from mcp_server.google_drive import read_google_drive

#create mcp server
mcp = FastMCP(
    "Google Drive Content Server"
)

#Create mcp tool
@mcp.tool()
def get_lesson_content(file_id: str):

    """
    Retrieve lesson content from Google Drive
    """

    content = read_google_drive(file_id)

    return content

#start MCP
if __name__ == "__main__":
    mcp.run()