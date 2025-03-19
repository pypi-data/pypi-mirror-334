from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import mcp_web_search.search as search
from langchain_core.documents import Document
import os
import asyncio


async def create_rag(links: list[str]) -> FAISS:
    try:
        model_name = os.getenv("MODEL")
        embeddings = OpenAIEmbeddings(
            model=model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_API_BASE"),
            chunk_size=64
        )
        documents = []
        # 使用asyncio.gather并行处理所有URL请求
        tasks = [search.get_web_content(url) for url in links]
        results = await asyncio.gather(*tasks)
        for result in results:
            documents.extend(result)
        
        # 文本分块处理
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=500,
            length_function=len,
            is_separator_regex=False,
        )
        split_documents = text_splitter.split_documents(documents)
        # print(documents)
        vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)
        return vectorstore
    except Exception as e:
        print(f"Error in create_rag: {str(e)}")
        raise

async def create_rag_from_documents(documents: list[Document]) -> FAISS:
    """
    直接从文档列表创建RAG系统，避免重复抓取网页
    
    Args:
        documents: 已经获取的文档列表
        
    Returns:
        FAISS: 向量存储对象
    """
    try:
        model_name = os.getenv("MODEL")
        embeddings = OpenAIEmbeddings(
            model=model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_API_BASE"),
            chunk_size=64
        )
        
        # 文本分块处理
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=500,
            length_function=len,
            is_separator_regex=False,
        )
        split_documents = text_splitter.split_documents(documents)
        
        vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)
        return vectorstore
    except Exception as e:
        print(f"Error in create_rag_from_documents: {str(e)}")
        raise

async def search_rag(query: str, vectorstore: FAISS) -> list[Document]:
    return vectorstore.similarity_search(query, k=3)

