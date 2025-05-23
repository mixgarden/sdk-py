# mixgarden

Async Python client for the **Mixgarden** AI‑plugin platform.

![PyPI](https://img.shields.io/pypi/v/mixgarden)
![Status](https://img.shields.io/pypi/status/mixgarden)
![License](https://img.shields.io/pypi/l/mixgarden)

---

## Install

```bash
python -m pip install mixgarden
```

Supports Python 3.9 – 3.12.

---

## Usage

```python
import asyncio
from mixgarden import Mixgarden

async def main():
    mg = Mixgarden(api_key="sk-…")

    resp = await mg.chat(
        "Give me three business‑name ideas for a coffee shop",
        plugin_id="creativity-plus"
    )
    print(resp["text"])

asyncio.run(main())
```

The client uses **httpx** and is fully async.

---

## Client reference

| Method | Description |
| ------ | ----------- |
| `Mixgarden(api_key, base_url=None)` | create a client |
| `await chat(prompt, plugin_id, model=None, **params)` | run a plugin |
| `await list_plugins()` | list visible plugins |
| `await get_plugin(plugin_id)` | fetch plugin metadata |

---

## Examples

* `examples/basic.py` – one‑off chat  
* `examples/fastapi_app.py` – integrate inside a FastAPI route

---

## Development

```bash
git clone https://github.com/mixgarden/sdk-py.git
cd sdk-py
python -m pip install -e ".[dev]"
pytest
```

Run `ruff` and `black` before opening a PR.

---

## Publishing (maintainers)

```bash
python -m build
python -m twine upload dist/*
```

---

## License

MIT
