"""HTTP 客户端模块

提供同步和异步 HTTP 客户端实现，基于 httpx 库封装常用功能。

特性：
- 统一请求入口 (request 方法)
- 自动重试机制
- 智能响应解析
- 流式响应支持
- 类型注解完善

示例代码：
----------
# 同步客户端
with HttpClient("https://api.example.com") as client:
    response = client.get("/data")
    print(response)

# 异步客户端
async with AsyncHttpClient("https://api.example.com") as client:
    response = await client.get("/data")
    print(response)
"""

import httpx
from typing import Dict, Optional, Union


# 同步请求客户端
class HttpClient:
    """同步 HTTP 客户端
    
    封装常用 HTTP 操作，支持自动重试和智能响应解析。

    Attributes:
        base_url (str): 基础请求地址 (e.g. "https://api.example.com")
        headers (Dict[str, str]): 默认请求头
        timeout (int): 请求超时时间（秒），默认 10
        max_retries (int): 最大重试次数，默认 3

    Example:
        >>> with HttpClient("https://httpbin.org") as client:
        ...     resp = client.get("/get")
        ...     print(resp.status_code)
        200
    """

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 10,
        max_retries: Optional[int] = 3,
    ):
        """初始化同步客户端

        Args:
            base_url: 基础请求地址
            headers: 自定义请求头，默认为空字典
            timeout: 超时时间（秒），设为 None 表示不限制
            max_retries: 失败请求最大重试次数
        """
        # 初始化配置
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.max_retries = max_retries

        # 实例化同步客户端
        self.client = httpx.Client(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
        )

    def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        data: Optional[Union[Dict, str, bytes]] = None,
        json: Optional[Dict] = None,
        stream: Optional[bool] = False,
    ) -> Union[Dict, str, bytes, httpx.Response]:
        """执行 HTTP 请求

        参数：
            method: HTTP 方法 (GET/POST/PUT等)
            url: 请求路径（自动拼接基础URL）
            params: URL 查询参数
            data: 请求体数据（表单/二进制）
            json: JSON 格式请求体
            stream: 是否返回原始流式响应

        返回：
            根据 Content-Type 自动解析的响应内容：
            - application/json → Dict
            - 其他类型 → str/bytes
            如果 stream=True 返回 httpx.Response 对象

        异常：
            连续失败 max_retries 次后返回 None
            可通过 response.raise_for_status() 手动抛出异常
        """
        url = f"{self.base_url}/{url.lstrip('/')}"
        for _ in range(self.max_retries):
            try:
                with self.client.stream(
                    method,
                    url,
                    params=params,
                    data=data,
                    json=json,
                    headers=self.headers,
                    timeout=self.timeout,
                ) as response:
                    response.raise_for_status()
                    return self._handle_response(response, stream)
            except httpx.HTTPStatusError as e:
                print(f"HTTP Error: {e}")
            except httpx.RequestError as e:
                print(f"Request Error: {e}")
        return None

    def _handle_response(self, response: httpx.Response, stream: bool = False):
        """处理同步相应"""
        if stream:
            return response
        response.read()  # 显式读取响应内容
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()
        return response.text

    def get(
        self, url: str, params: Optional[Dict] = None, stream: Optional[bool] = False
    ):
        """同步GET请求封装"""
        return self.request("GET", url, params=params, stream=stream)

    def post(
        self,
        url: str,
        params: Optional[Dict] = None,
        data: Optional[Union[Dict, str, bytes]] = None,
        json: Optional[Dict] = None,
        stream: Optional[bool] = False,
    ):
        """同步POST请求封装"""
        return self.request(
            "POST", url, params=params, data=data, json=json, stream=stream
        )

    def close(self):
        """关闭会话"""
        self.client.close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 异步请求客户端
class AsyncHttpClient:
    """异步 HTTP 客户端

    接口与同步客户端一致，所有方法需使用 await 调用

    Example:
        >>> async with AsyncHttpClient("https://httpbin.org") as client:
        ...     resp = await client.get("/get")
        ...     print(resp.status_code)
        200
    """

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 10,
        max_retries: Optional[int] = 3,
    ):
        # 初始化配置
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.max_retries = max_retries

        # 实例化异步客户端
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
        )

    async def arequest(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        data: Optional[Union[Dict, str, bytes]] = None,
        json: Optional[Dict] = None,
        stream: Optional[bool] = False,
    ) -> Union[Dict, str, bytes, httpx.Response]:
        """执行异步 HTTP 请求

        参数与返回值同同步客户端，需使用 await 调用
        """
        url = f"{self.base_url}/{url.lstrip('/')}"
        for _ in range(self.max_retries):
            try:
                async with self.client.stream(
                    method,
                    url,
                    params=params,
                    data=data,
                    json=json,
                    headers=self.headers,
                    timeout=self.timeout,
                ) as response:
                    response.raise_for_status()
                    return await self._handle_response(response, stream)
            except httpx.HTTPStatusError as e:
                print(f"HTTP Error: {e}")
            except httpx.RequestError as e:
                print(f"Request Error: {e}")
        return None

    async def _handle_response(self, response: httpx.Response, stream: bool = False):
        """处理异步相应"""
        if stream:
            return response
        await response.aread()  # 显式读取响应内容
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()
        return response.text()

    async def aget(
        self, url: str, params: Optional[Dict] = None, stream: Optional[bool] = False
    ):
        """异步GET请求封装"""
        return await self.arequest("GET", url, params=params, stream=stream)

    async def apost(
        self,
        url: str,
        params: Optional[Dict] = None,
        data: Optional[Union[Dict, str, bytes]] = None,
        json: Optional[Dict] = None,
        stream: Optional[bool] = False,
    ):
        """异步POST请求封装"""
        return await self.arequest(
            "POST", url, params=params, data=data, json=json, stream=stream
        )

    async def aclose(self):
        """关闭会话"""
        await self.client.aclose()

    async def __aenter__(self):
        """异步上下文管理器"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出时关闭会话"""
        await self.aclose()
