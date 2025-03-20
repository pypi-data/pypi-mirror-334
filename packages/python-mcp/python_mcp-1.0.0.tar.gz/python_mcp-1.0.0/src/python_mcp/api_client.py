"""
Worker API 客户端
负责处理与 Cloudflare Worker API 的通信
包含超时控制、重试机制和缓存功能
"""

import time
import logging
import requests
from typing import Any, Dict, List, Optional, Tuple, Union
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("api_client")

class WorkerApiClient:
    def __init__(self, base_url: str, timeout: int = 30, retries: int = 3, cache_ttl: int = 60000):
        """初始化API客户端
        
        Args:
            base_url: Cloudflare Worker API的基础URL
            timeout: 请求超时时间（秒）
            retries: 重试次数
            cache_ttl: 缓存有效期（毫秒）
        """
        self.base_url = base_url
        self.timeout = timeout
        self.cache = {}
        self.cache_ttl = cache_ttl  # 缓存有效期（毫秒）
        
        # 创建带有重试机制的会话
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=retries,
            backoff_factor=1,  # 每次重试间隔增加1秒
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        # 应用重试策略到session
        self.session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
        self.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        
        # 设置默认请求头
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "Python-Requests/WorkerApiClient-1.0"
        })
        
        logger.info(f"初始化API客户端: URL={base_url}, 超时={timeout}秒")

    def get_from_cache(self, key: str, fetcher_func):
        """从缓存获取数据或调用fetcher_func获取新数据
        
        Args:
            key: 缓存键
            fetcher_func: 获取数据的函数
            
        Returns:
            缓存的数据或新获取的数据
        """
        now = int(time.time() * 1000)  # 当前时间（毫秒）
        
        if key in self.cache:
            cached_data, timestamp = self.cache[key]
            if now - timestamp < self.cache_ttl:
                logger.info(f"使用缓存数据: {key}")
                return cached_data
        
        logger.info(f"获取新数据: {key}")
        data = fetcher_func()
        self.cache[key] = (data, now)
        return data

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """发送HTTP请求到Worker API
        
        Args:
            method: HTTP方法
            endpoint: API端点
            **kwargs: 传递给requests的其他参数
            
        Returns:
            Response对象
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"发起{method}请求: {url}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            
            logger.info(f"请求成功: 状态={response.status_code}")
            return response
            
        except requests.RequestException as e:
            logger.error(f"请求失败: {str(e)}")
            raise

    def get_all_prompts(self) -> List[Dict[str, Any]]:
        """获取所有提示词
        
        Returns:
            提示词列表
        """
        def fetcher():
            logger.info(f"获取所有提示词，API路径: /tasks")
            response = self.request("GET", "/tasks")
            response.raise_for_status()
            prompts = response.json()
            logger.info(f"成功获取{len(prompts)}个提示词")
            return prompts
            
        return self.get_from_cache("all_prompts", fetcher)
        
    def get_prompt_by_name(self, name: str) -> Dict[str, Any]:
        """根据名称获取提示词
        
        Args:
            name: 提示词名称
            
        Returns:
            提示词详情
        """
        def fetcher():
            all_prompts = self.get_all_prompts()
            prompt = next((p for p in all_prompts if p.get("name") == name), None)
            
            if not prompt:
                raise ValueError(f"未找到名称为 '{name}' 的提示词")
                
            logger.info(f"找到提示词: {name}")
            return prompt
            
        return self.get_from_cache(f"prompt_{name}", fetcher) 