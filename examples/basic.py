"""examples/basic.py
Minimal Python demo for the Mixgarden SDK

Install:
    python -m pip install mixgarden

Run:
    python examples/basic.py
"""

import asyncio
from mixgarden import Mixgarden


async def main() -> None:
    mg = Mixgarden(api_key="sk-your-key")  # replace with your real key
    resp = await mg.chat(
        "Rewrite this in pirate slang",
        plugin_id="tonepro",
    )
    print(resp["text"])


if __name__ == "__main__":
    asyncio.run(main())
