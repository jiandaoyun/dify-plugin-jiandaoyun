import json
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.httpclient import APIRequestTool
from utils.json2table import json2table


class GetEntryTool(Tool):
    #获取app下全部表单信息
    '''
    @请求参数：
    {
        "app_id": "应用ID",
        "limit": 100,  # 可选，默认100
        "offset": 0    # 可选，默认0
    }
    '''
    def getEntryList(self, data: dict[str, Any],base_url:str) -> dict[str, Any]:
        try:
            access_token = self.runtime.credentials["jiandaoyun_api_key"]
        except KeyError:
            raise Exception("简道云 Access Token 未配置或无效。请在插件设置中提供。")
        httpClient = APIRequestTool(base_url=base_url, token=access_token)
        return httpClient.create("/v5/app/entry/list", data=data)

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # get app_id from tool_parameters
        app_id = tool_parameters.get("app_id")
        if not app_id:
            raise ValueError("app_id 不能为空")
        # try to get limit and offset from tool_parameters, if not provided, use default values
        limit = tool_parameters.get("limit", 100)
        offset = tool_parameters.get("offset", 0)
        output_type = tool_parameters.get("output_type", "json")
        response = self.getEntryList({
            "app_id": app_id,
            "limit": limit,
            "offset": offset
        },tool_parameters.get("base_url"))
        if response.get("status") != "success":
            raise ValueError(f"获取表单列表失败: {response.get('message', '未知错误')}")
        response = response.get("data")
        json_data = {
            "status": "success",
            "data": response,
            "message": "获取表单列表成功"
        }
        try:
            dumped_data = json.dumps(json_data)
        except json.JSONDecodeError:
            raise ValueError("返回的数据不是有效的 JSON 格式")
        # yield self.create_json_message(json_data)
        if output_type == "json":
            yield self.create_text_message(dumped_data)
        elif output_type == "table":
            output_data = json2table(response["forms"])
            yield self.create_text_message(output_data)