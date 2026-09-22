# statoly

Official Python client for the [Statoly](https://statoly.ch) API.

```bash
pip install statoly
```

```python
import asyncio, os
from statoly import Statoly

async def main():
    statoly = Statoly(os.environ["STATOLY_TOKEN"])

    for monitor in await statoly.monitors.get():
        print(monitor.title, monitor.status)

asyncio.run(main())
```

The client is asynchronous. Point it elsewhere with
`Statoly(token, base_url="https://…")`; `statoly.api` exposes the full
generated fluent API.

Generated from the Statoly OpenAPI document with Microsoft Kiota. Report issues
at [statoly/sdks](https://github.com/statoly/sdks). MIT.
