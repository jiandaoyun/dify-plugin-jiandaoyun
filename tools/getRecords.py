import json
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.httpclient import APIRequestTool
from utils.json2table import json2table


class DatagetlistTool(Tool):

    def getDataList(self, data: dict[str, Any],base_url) -> dict[str, Any]:
        try:
            access_token = self.runtime.credentials["jiandaoyun_api_key"]
        except KeyError:
            raise Exception("简道云 Access Token 未配置或无效。请在插件设置中提供。")
        httpClient = APIRequestTool(base_url=base_url, token=access_token)
        return httpClient.create("v5/app/entry/data/list", data=data)["data"]


    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        app_id = tool_parameters.get("app_id", "")
        if not app_id:
            raise ValueError("app_id 不能为空")
        entry_id = tool_parameters.get("entry_id", "")
        if not entry_id:
            raise ValueError("entry_id 不能为空")
        output_type = tool_parameters.get("output_type", "json")
        data = self.getDataList({
            "app_id": app_id,
            "entry_id": entry_id,
            "data_id": tool_parameters.get("data_id", None),
            "fields":  tool_parameters.get("fields", None),
            # array形式的字段列表，若不传则返回全部字段,
            "filter": tool_parameters.get("filter", "{}"),  # 字段过滤条件，json格式
            "limit": tool_parameters.get("limit", 10),  # 默认100条
        },tool_parameters.get("base_url"))
        json_data = {
            "status": "success",
            "data": data,
            "message": "获取数据列表成功"
        }
        try:
            json_str = json.dumps(json_data)
        except json.JSONDecodeError:
            raise ValueError("返回的数据不是有效的 JSON 格式")
        if output_type == "table":
            output_data = json2table(data["data"])
            yield self.create_text_message(output_data)
        elif output_type == "json":
            yield self.create_text_message(json_str)