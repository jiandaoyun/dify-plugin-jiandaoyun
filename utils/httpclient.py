import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin


class APIRequestTool:
    def __init__(self, base_url: str, token: str):
        """
        初始化请求工具，设置基础 URL 和用户 token。

        Args:
            base_url (str): API 的基础 URL，例如 "https://api.example.com/"
            token (str): 用户的认证 token
        """
        if not base_url:
            self.base_url = "https://api.jiandaoyun.com/api/"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def make_request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        通用请求方法，支持 GET、POST、PUT、PATCH、DELETE 等。

        Args:
            method (str): HTTP 方法（get, post, put, patch, delete）
            endpoint (str): API 端点路径，例如 "create" 或 "delete/123"
            params (dict, optional): 查询参数
            data (dict, optional): 请求体数据（JSON 格式）

        Returns:
            dict: 包含状态、数据和消息的响应
        """
        # 拼接完整 URL
        url = urljoin(self.base_url, endpoint.lstrip("/"))

        try:
            # 发起请求
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=10  # 设置超时时间
            )

            # 检查响应状态
            response.raise_for_status()

            # 尝试解析 JSON 响应
            try:
                response_data = response.json()
            except ValueError:
                response_data = {"raw_response": response.text}

            return {
                "status": "success",
                "data": response_data,
                "message": "Request completed successfully"
            }

        except requests.exceptions.HTTPError as http_err:
            return {
                "status": "error",
                "data": None,
                "message": f"HTTP error occurred: {str(http_err)}"
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "data": None,
                "message": "Failed to connect to the server"
            }
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "data": None,
                "message": "Request timed out"
            }
        except requests.exceptions.RequestException as req_err:
            return {
                "status": "error",
                "data": None,
                "message": f"Request failed: {str(req_err)}"
            }

    def create(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """封装 POST 请求，用于创建资源"""
        return self.make_request("POST", endpoint, data=data)

    def read(self, endpoint: str, params: Optional[Dict[str, Any]] = None,data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """封装 GET 请求，用于查询资源"""
        return self.make_request("GET", endpoint, params=params,data=data)

    def update(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """封装 PUT 请求，用于更新资源"""
        return self.make_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """封装 DELETE 请求，用于删除资源"""
        return self.make_request("DELETE", endpoint)