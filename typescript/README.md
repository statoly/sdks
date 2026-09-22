# @statoly/sdk

Official TypeScript client for the [Statoly](https://statoly.ch) API.

```bash
npm install @statoly/sdk
```

```ts
import { Statoly } from '@statoly/sdk';

const statoly = new Statoly(process.env.STATOLY_TOKEN!);

const monitors = await statoly.monitors.get();

for (const monitor of monitors ?? []) {
  console.log(monitor.title, monitor.status);
}
```

Point it elsewhere with `new Statoly(token, { baseUrl: 'https://…' })`.
`statoly.api` exposes the full generated fluent API.

Generated from the Statoly OpenAPI document with Microsoft Kiota. Report issues
at [statoly/sdks](https://github.com/statoly/sdks). MIT.
