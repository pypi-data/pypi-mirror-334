"""
MCP 服务器
基于Model Context Protocol的Python SDK实现
"""

import logging
import os
import json
from typing import Dict, Any, List, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("错误: 未找到MCP库，请先安装依赖: pip install mcp")
    print("如果您在虚拟环境中运行，请确保已激活虚拟环境")
    import sys
    sys.exit(1)

from python_mcp.api_client import WorkerApiClient

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp_server")

# 配置选项
CONFIG = {
    "WORKER_URL": "https://polished-math-2b32.zhongce-xie.workers.dev",
    "API_TIMEOUT": 60,  # 秒
    "RETRIES": 3,
}

logger.info(f"启动配置: WORKER_URL={CONFIG['WORKER_URL']}, API_TIMEOUT={CONFIG['API_TIMEOUT']}秒")

# 创建API客户端
api_client = WorkerApiClient(CONFIG["WORKER_URL"], CONFIG["API_TIMEOUT"], CONFIG["RETRIES"])

# 创建MCP服务器
mcp = FastMCP("作图 Prompt 管理服务")

@mcp.tool()
def mcp__get_all_names() -> Dict[str, Any]:
    """获取所有提示词的名称
    
    Returns:
        JSON格式的提示词名称列表
    """
    try:
        logger.info("获取所有提示词名称...")
        
        all_prompts = api_client.get_all_prompts()
        logger.info(f"成功获取提示词列表: 共{len(all_prompts)}个")
        
        names = [p.get("name") for p in all_prompts]
        
        result = {
            "status": "success",
            "message": "成功获取所有提示词名称",
            "data": names
        }
        
        logger.info("返回提示词名称列表")
        return result
    except Exception as e:
        logger.error(f"获取提示词名称出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        error_result = {
            "status": "error",
            "message": f"获取所有提示词名称失败: {str(e)}"
        }
        
        return error_result

@mcp.tool()
def mcp__get_content_by_name(name: str) -> Dict[str, Any]:
    """根据名称获取提示词内容
    
    Args:
        name: 提示词名称
        
    Returns:
        提示词详情
    """
    try:
        logger.info(f"通过名称获取提示词内容 (名称: \"{name}\")...")
        
        prompt = api_client.get_prompt_by_name(name)
        logger.info(f"成功获取提示词内容: {name}")
        
        result = {
            "status": "success",
            "message": f"成功获取名称为 \"{name}\" 的提示词内容",
            "data": {
                "id": prompt.get("id"),
                "name": prompt.get("name"),
                "content": prompt.get("content"),
                "category": prompt.get("category", ""),
                "description": prompt.get("description", "")
            }
        }
        
        return result
    except Exception as e:
        logger.error(f"获取提示词内容出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        error_result = {
            "status": "error",
            "message": f"通过名称获取提示词内容失败: {str(e)}"
        }
        
        return error_result

# 如果直接运行此脚本，启动MCP服务器
def main():
    logger.info("正在启动MCP Prompt管理服务器...")
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"启动服务器时出错: {str(e)}")

if __name__ == "__main__":
    main() 