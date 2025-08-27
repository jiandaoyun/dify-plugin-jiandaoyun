from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class JiandaoyunProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """response = requests.get("https://api.jiandaoyun.com/api/health_check ", headers={"Authorization": f"Bearer {api_key}"})
            if response.status_code != 200:
                raise ValueError("API Key 无效，请重新输入")"""
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
