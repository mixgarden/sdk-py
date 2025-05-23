"""mixgarden/client.py
Async Python client for the Mixgarden plugin API.
Usage:
    from mixgarden import Mixgarden
    mg = Mixgarden(api_key="sk-...")
    data = await mg.chat("Hello", plugin_id="tonepro")
"""

from __future__ import annotations

import httpx
from typing import Any, Dict, Optional


class Mixgarden:
    """Minimal async SDK client."""

    __slots__ = ("_key", "_base_url", "client")

    def __init__(self, api_key: str, base_url: str | None = None) -> None:
        self._key = api_key
        self._base_url = base_url or "https://api.mixgarden.ai/v1"
        self.client = httpx.AsyncClient(
            base_url=self._base_url,
            headers={"Authorization": f"Bearer {self._key}"},
            timeout=20,
        )

    # --------------------------------------------------------------------- #
    # public API methods
    # --------------------------------------------------------------------- #

    async def chat(
        self,
        prompt: str,
        /,
        *,
        plugin_id: str,
        model: str | None = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Run *prompt* through a plugin and return the JSON response."""
        payload: Dict[str, Any] = {
            "prompt": prompt,
            "pluginId": plugin_id,
        }
        if model:
            payload["model"] = model
        if params:
            payload["params"] = params

        r = await self.client.post("/chat", json=payload)
        r.raise_for_status()
        return r.json()

    async def list_plugins(self) -> Dict[str, Any]:
        """Return all plugins visible to the current API key."""
        r = await self.client.get("/plugins")
        r.raise_for_status()
        return r.json()

    async def get_plugin(self, plugin_id: str) -> Dict[str, Any]:
        """Fetch metadata for a single plugin."""
        r = await self.client.get(f"/plugins/{plugin_id}")
        r.raise_for_status()
        return r.json()

    # --------------------------------------------------------------------- #
    # convenience helpers
    # --------------------------------------------------------------------- #

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self.client.aclose()

    # ------------------------------------------------------ context manager

    async def __aenter__(self) -> "Mixgarden":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        await self.close()


__all__ = ["Mixgarden"]
