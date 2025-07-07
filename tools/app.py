import json
from collections.abc import Generator
from typing import Any, Dict

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.httpclient import APIRequestTool


class AppTool(Tool):

    def get_app_list(self,data)->Dict[str, Any]:
        try:
            access_token = self.runtime.credentials["jiandaoyun_api_key"]
        except KeyError:
            raise Exception("简道云 Access Token 未配置或无效。请在插件设置中提供。")
        httpClient = APIRequestTool(base_url="https://api.jiandaoyun.com/api", token=access_token)
        return httpClient.create("v5/app/list",data=data)["data"]

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        data = {"limit": tool_parameters["limit"]}
        response = self.get_app_list(data=data)
        json_data = {
            "status": "success",
            "data": response,
            "message": "获取应用列表成功"
        }
        yield self.create_json_message(json_data)
        concat_data = json.dumps(response, ensure_ascii=False, indent=2)
        yield self.create_text_message(concat_data)