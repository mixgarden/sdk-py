import os
from typing import Any, Dict, Optional

import httpx


class MixgardenSDK:
    """Very small Python wrapper around the Mixgarden REST API."""

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.mixgarden.ai/api/v1") -> None:
        self.api_key = api_key or os.getenv("MIXGARDEN_API_KEY")
        if not self.api_key:
            raise ValueError("Mixgarden API key missing (set MIXGARDEN_API_KEY or pass api_key).")
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={ "Authorization": f"Bearer {self.api_key}" },
            timeout=30.0,
        )

    # ---- internal -------------------------------------------------------
    def _request(self, method: str, path: str, *, json: Optional[dict] = None, params: Optional[dict] = None):
        response = self._client.request(method.upper(), path, json=json, params=params)
        response.raise_for_status()
        if response.status_code == 204:
            return None
        return response.json()

    # ---- public helpers -------------------------------------------------
    def get_models(self):
        return self._request("GET", "/models")

    def chat(self, **params):
        conversation_id = params.pop("conversationId", None)
        if conversation_id:
            # Add message to existing conversation
            self._request(
                "POST",
                f"/conversations/{conversation_id}/messages",
                json=params
            )
            # Return updated conversation (with messages)
            return self.get_conversation(conversation_id)
        else:
            # Create a new conversation
            convo_res = self._request(
                "POST",
                "/conversations",
                json=params
            )
            conversation_id = convo_res["id"]
            # Add first message
            message_params = {
                "model": params.get("model"),
                "pluginId": params.get("pluginId"),
                "pluginSettings": params.get("pluginSettings"),
                "content": params.get("content"),
            }
            self._request(
                "POST",
                f"/conversations/{conversation_id}/messages",
                json=message_params
            )
            # Return updated conversation (with messages)
            return self.get_conversation(conversation_id)

    def get_completion(self, **params):
        return self._request("POST", "/chat/completions", json=params)

    def get_mg_completion(self, **params):
        return self._request("POST", "/mg-completion", json=params)

    def get_plugins(self):
        return self._request("GET", "/plugins")

    def get_conversations(self, **params):
        return self._request("GET", "/conversations", params=params)

    def get_conversation(self, conversation_id: str):
        return self._request("GET", f"/conversations/{conversation_id}")

    def close(self):
        self._client.close()
