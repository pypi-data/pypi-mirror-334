from typing import Any, Optional
import asyncio
from mcp.server.fastmcp import FastMCP
import mcp_web_search.rag as rag
import mcp_web_search.search as search
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mcp = FastMCP("web_search", timeout=114514.0)

@mcp.tool()
async def search_web_tool(query: str) -> str:
    logger.info(f"Searching web for query: {query}")
    results = await search.search_web(query)
    vectorstore = await rag.create_rag([result.url for result in results])
    return '\n---\n'.join(doc.page_content for doc in await rag.search_rag(query, vectorstore))

@mcp.tool()
async def get_web_content_tool(url: str) -> str:
    try:
        documents = await asyncio.wait_for(search.get_web_content(url), timeout=15.0)
        if documents:
            return '\n\n'.join([doc.page_content for doc in documents])
        return "无法获取网页内容。"
    except asyncio.TimeoutError:
        return "获取网页内容超时，请稍后重试。"
    except Exception as e:
        return f"获取网页内容时发生错误: {str(e)}"

def main():
    asyncio.run(mcp.run(transport="stdio"))