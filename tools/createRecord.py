import json
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.httpclient import APIRequestTool


class CreateRecordTool(Tool):
    '''
    @请求参数：
    {
      "app_id": "",
      "entry_id": "",
      "data_id": ""
    }
    '''
    def create_data(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            access_token = self.runtime.credentials["jiandaoyun_api_key"]
        except KeyError:
            raise Exception("简道云 Access Token 未配置或无效。请在插件设置中提供。")
        httpClient = APIRequestTool(base_url="https://api.jiandaoyun.com/api", token=access_token)
        return httpClient.create("v5/app/entry/data/create", data=data)["data"]



    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        app_id = tool_parameters.get("app_id", "")
        if not app_id:
            raise ValueError("app_id 不可为空")
        entry_id = tool_parameters.get("entry_id", None)
        if not entry_id:
            raise ValueError("entry_id 不可为空")
        data = tool_parameters['data']# string形式的json，因此处理时候需要解析
        try:
            loaded_data = json.loads(data)
        except json.JSONDecodeError:
            raise ValueError("data 参数必须是有效的 JSON 字符串")
        data = self.create_data({"app_id": app_id, "entry_id": entry_id, "data":loaded_data })
        json_data = {
            "status": "success",
            "data": data,
            "message": "创建数据成功"
        }
        # yield self.create_json_message(json_data)
        yield self.create_text_message(str(json_data))

