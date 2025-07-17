import json
from collections.abc import Generator
from typing import Any, Dict

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.httpclient import APIRequestTool
from utils.json2table import json2table


class AppTool(Tool):


    def get_app_list(self,data:Dict[str,Any],base_url:str)->Dict[str, Any]:
        try:
            access_token = self.runtime.credentials["jiandaoyun_api_key"]
        except KeyError:
            raise Exception("简道云 Access Token 未配置或无效。请在插件设置中提供。")
        httpClient = APIRequestTool(base_url=base_url, token=access_token)
        return httpClient.create("v5/app/list",data=data)

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        limit = tool_parameters.get("limit", 10)
        offset = tool_parameters.get("offset", 0)
        output_type = tool_parameters.get("output_type", "json")

        response = self.get_app_list({"limit": limit, "skip": offset},tool_parameters.get("base_url"))
        if response.get("status") != "success":
            raise ValueError(f"获取应用列表失败: {response.get('message', '未知错误')}")
        response = response.get("data")
        # yield self.create_json_message(json_data)
        if output_type == "json":
            concat_data = json.dumps(response, ensure_ascii=False, indent=2)
            yield self.create_text_message(concat_data)
        elif output_type == "table":
            output_data = json2table(response["apps"])
            yield self.create_text_message(output_data)
        else:
            raise ValueError(f"不支持的输出类型: {output_type}，请使用 'json' 或 'table'。")