from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class WidgetTool(Tool):

    def getWidget(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            access_token = self.runtime.credentials["jiandaoyun_api_key"]
        except KeyError:
            raise Exception("简道云 Access Token 未配置或无效。请在插件设置中提供。")

        httpClient = self.runtime.get_http_client(base_url="https://api.jiandaoyun.com/api", token=access_token)
        return httpClient.create("v5/app/entry/widget/list", data=data)["data"]


    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        data = self.getWidget(tool_parameters)
        yield self.create_json_message({
            "result": "Hello, world!"
        })