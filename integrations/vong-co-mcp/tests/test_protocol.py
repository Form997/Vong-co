"""In-memory MCP protocol smoke test (requires mcp>=2)."""
import unittest

from mcp import Client
from server import mcp


class MCPProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_tool_discovery_and_list(self):
        async with Client(mcp, raise_exceptions=True) as client:
            result = await client.list_tools()
            names = {item.name for item in result.tools}
            self.assertEqual(
                names,
                {
                    "list_ban_to",
                    "search_ban_to",
                    "get_ban_to",
                    "get_nghiem_thu",
                    "get_di_ban",
                    "get_nguon",
                    "get_quy_che_v2",
                },
            )
            output = await client.call_tool("list_ban_to", {})
            self.assertFalse(output.is_error)
            self.assertEqual(output.structured_content["total"], 20)


if __name__ == "__main__":
    unittest.main()
