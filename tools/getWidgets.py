import json
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.httpclient import APIRequestTool


class WidgetTool(Tool):

    def getWidget(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            access_token = self.runtime.credentials["jiandaoyun_api_key"]
        except KeyError:
            raise Exception("简道云 Access Token 未配置或无效。请在插件设置中提供。")

        httpClient = APIRequestTool(base_url="https://api.jiandaoyun.com/api", token=access_token)
        return httpClient.create("v5/app/entry/widget/list", data=data)["data"]


    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        app_id = tool_parameters.get("app_id", "")
        if not app_id:
            raise ValueError("app_id 不能为空")
        entry_id = tool_parameters.get("entry_id", "")
        if not entry_id:
            raise ValueError("entry_id 不能为空")
        widget_data = self.getWidget({"app_id": app_id, "entry_id": entry_id})
        try:
            dumped_data = json.dumps(widget_data)
        except json.JSONDecodeError:
            raise ValueError("返回的数据不是有效的 JSON 格式")
        data = {
            "status": "success",
            "data": widget_data,
            "message": "获取字段列表成功"
        }
        # yield self.create_json_message(data)
        yield self.create_text_message(str(dumped_data))
