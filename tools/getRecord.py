import json
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.httpclient import APIRequestTool
from utils.json2table import json2table


class DatagetTool(Tool):
    '''
    @请求参数：
    {
      "app_id": "",
      "entry_id": "",
      "data_id": ""
    }
    '''
    def get_data(self, data: dict[str, Any],base_url:str) -> dict[str, Any]:
        try:
            access_token = self.runtime.credentials["jiandaoyun_api_key"]
        except KeyError:
            raise Exception("简道云 Access Token 未配置或无效。请在插件设置中提供。")
        httpClient = APIRequestTool(base_url=base_url, token=access_token)
        return httpClient.create("v5/app/entry/data/get", data=data)



    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        app_id = tool_parameters.get("app_id", "")
        if not app_id:
            raise ValueError("app_id 不能为空")
        entry_id = tool_parameters.get("entry_id", "")
        if not entry_id:
            raise ValueError("entry_id 不能为空")
        data_id = tool_parameters.get("data_id", None)
        if not data_id:
            raise ValueError("data_id 不能为空")
        output_type = tool_parameters.get("output_type", "json")
        response = self.get_data({
            "app_id": app_id,
            "entry_id": entry_id,
            "data_id": data_id
        },tool_parameters.get("base_url"))
        if response.get("status") != "success":
            raise ValueError(f"获取数据失败: {response.get('message', '未知错误')}")
        response_data = response["data"]
        try:
            json_data = json.dumps(response_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("返回的数据不是有效的 JSON 格式")
        if output_type == "json":
            yield self.create_text_message(json_data)
        elif output_type == "table":
            table_data = json2table(response_data["data"])
            yield self.create_text_message(table_data)

