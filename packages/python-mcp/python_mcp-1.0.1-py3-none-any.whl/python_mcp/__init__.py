"""
Python MCP 提示词管理服务

基于 Model Context Protocol 的 Python SDK 实现，
用于连接 Cloudflare Worker API 获取提示词数据。
"""

__version__ = "1.0.1"

from python_mcp.api_client import WorkerApiClient
from python_mcp.mcp_server import mcp, main