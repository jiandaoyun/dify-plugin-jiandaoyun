from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage



class JiandaoyunTool(Tool):
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
        httpClient = self.runtime.get_http_client(base_url="https://api.jiandaoyun.com/api", token=access_token)
        return httpClient.create("v5/app/entry/data/get", data=data)["data"]



    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        app_id = tool_parameters["app_id"]
        entry_id = tool_parameters.get("entry_id", None)
        data_id = tool_parameters.get("data_id", None)

        data = self.get_data({"app_id": app_id, "entry_id": entry_id, "data_id": data_id})
        json_data = {
            "status": "success",
            "data": data,
            "message": "获取数据成功"
        }
        yield self.create_json_message(json_data)
        yield self.create_text_message(str(data))

