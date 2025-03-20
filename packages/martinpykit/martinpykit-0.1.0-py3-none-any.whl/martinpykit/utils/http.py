import httpx
from typing import Dict, Optional, Union


# 同步请求客户端
class HttpClient:
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
        """同步请求封装"""
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


# 异步请求客户端
class AsyncHttpClient:
    """异步HTTP客户端"""

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

    async def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        data: Optional[Union[Dict, str, bytes]] = None,
        json: Optional[Dict] = None,
        stream: Optional[bool] = False,
    ) -> Union[Dict, str, bytes, httpx.Response]:
        """异步请求封装"""
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

    async def get(
        self, url: str, params: Optional[Dict] = None, stream: Optional[bool] = False
    ):
        """异步GET请求封装"""
        return await self.request("GET", url, params=params, stream=stream)

    async def post(
        self,
        url: str,
        params: Optional[Dict] = None,
        data: Optional[Union[Dict, str, bytes]] = None,
        json: Optional[Dict] = None,
        stream: Optional[bool] = False,
    ):
        """异步POST请求封装"""
        return await self.request(
            "POST", url, params=params, data=data, json=json, stream=stream
        )

    async def close(self):
        """关闭会话"""
        await self.client.aclose()
