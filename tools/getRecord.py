from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.httpclient import APIRequestTool


class DatagetTool(Tool):
    '''
    @请求参数：
    {
      "app_id": "",
      "entry_id": "",
      "data_id": ""
    }
    '''
    def get_data(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            access_token = self.runtime.credentials["jiandaoyun_api_key"]
        except KeyError:
            raise Exception("简道云 Access Token 未配置或无效。请在插件设置中提供。")
        httpClient = APIRequestTool(base_url="https://api.jiandaoyun.com/api/", token=access_token)
        return httpClient.create("v5/app/entry/data/get", data=data)["data"]



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

        data = self.get_data({
            "app_id": app_id,
            "entry_id": entry_id,
            "data_id": data_id
        })

        # yield self.create_json_message(data)
        yield self.create_text_message(str(data))

