from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.httpclient import APIRequestTool


class EntrygetTool(Tool):
    #获取app下全部表单信息
    '''
    @请求参数：
    {
        "app_id": "应用ID",
        "limit": 100,  # 可选，默认100
        "offset": 0    # 可选，默认0
    }
    '''
    def getEntryList(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            access_token = self.runtime.credentials["jiandaoyun_api_key"]
        except KeyError:
            raise Exception("简道云 Access Token 未配置或无效。请在插件设置中提供。")
        httpClient = APIRequestTool(base_url="https://api.jiandaoyun.com/api", token=access_token)
        return httpClient.create("/v5/app/entry/list", data=data)["data"]

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # get app_id from tool_parameters
        app_id = tool_parameters["app_id"]
        # try to get limit and offset from tool_parameters, if not provided, use default values
        limit = tool_parameters.get("limit", 100)
        offset = tool_parameters.get("offset", 0)
        data = {
            "app_id": app_id,
            "limit": limit,
            "offset": offset
        }
        response = self.getEntryList(data)
        json_data = {
            "status": "success",
            "data": response,
            "message": "获取表单列表成功"
        }
        yield self.create_json_message(json_data)
