from pydantic import BaseModel
import httpx
from typing import Optional, List
import asyncio
import os
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_core.documents import Document

class SearchResult(BaseModel):
    url: str
    title: str

# Constants
TIMEOUT_SECONDS = 10.0
MAX_RETRIES = 3
FIRECRAWL_TIMEOUT = 20.0  # FireCrawl操作的超时时间

async def search_web(query: str, max_results: int = 3) -> Optional[list[SearchResult]]:
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
                response = await client.get(
                    f"{os.getenv("SEARXNG_API_BASE")}/search",
                    params={"q": query, "format": "json"}
                )
                response.raise_for_status()
                data = response.json()
                
                # Extract and convert results to SearchResult objects
                if data and "results" in data:
                    return [
                        SearchResult(url=result["url"], title=result["title"])
                        for result in data["results"][:max_results]
                    ]
                return []
                
        except httpx.TimeoutException:
            print(f"Request timed out (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(1)  # Wait 1 second before retrying
            continue
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    
    print("All retry attempts failed")
    return None

async def get_web_content(url: str) -> List[Document]:
    """
    获取网页内容并转换为文档列表
    
    Args:
        url: 要抓取的网页URL
        
    Returns:
        List[Document]: 文档列表
        
    Raises:
        TimeoutError: 如果抓取操作超时
        Exception: 如果抓取过程中发生其他错误
    """
    for attempt in range(MAX_RETRIES):
        try:
            # 创建FireCrawlLoader实例
            loader = FireCrawlLoader(
                url=url,
                mode="scrape"
            )
            
            # 使用超时保护
            documents = await asyncio.wait_for(loader.aload(), timeout=FIRECRAWL_TIMEOUT)
            
            # 如果成功获取文档，返回结果
            if documents and len(documents) > 0:
                return documents
            
            # 如果没有获取到文档，但没有发生异常，尝试重试
            print(f"No documents retrieved from {url} (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(1)  # 等待1秒后重试
                continue
                
        except asyncio.TimeoutError:
            print(f"FireCrawl operation timed out for {url} (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(1)
                continue
            raise  # 如果所有重试都失败，抛出异常
            
        except Exception as e:
            print(f"Error retrieving content from {url}: {str(e)} (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(1)
                continue
            raise  # 如果所有重试都失败，抛出异常
    
    # 如果所有重试都没有返回文档，返回空列表
    return []