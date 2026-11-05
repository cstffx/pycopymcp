"""Prueba extremo a extremo: cliente MCP real contra el servidor por stdio."""
import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def _call(content):
    params = StdioServerParameters(command=sys.executable, args=["-m", "pycopymcp"],
                                   env={**os.environ})
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = [t.name for t in (await s.list_tools()).tools]
            res = await s.call_tool("copy_to_clipboard", {"content": content})
            return tools, res


def test_lists_single_tool():
    tools, _ = asyncio.run(_call("x"))
    assert tools == ["copy_to_clipboard"]


def test_copy_via_mcp(paste):
    _, res = asyncio.run(_call("desde MCP 😀"))
    assert not res.isError
    assert paste().replace("\r\n", "\n").rstrip("\n") == "desde MCP 😀"


def test_empty_content_is_error():
    _, res = asyncio.run(_call(""))
    assert res.isError
