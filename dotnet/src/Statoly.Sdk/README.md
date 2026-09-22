# Statoly.Sdk

Official .NET client for the [Statoly](https://statoly.ch) API.

```bash
dotnet add package Statoly.Sdk
```

```csharp
using Statoly.Sdk;

var statoly = new StatolyClient(Environment.GetEnvironmentVariable("STATOLY_TOKEN")!);

foreach (var monitor in await statoly.Monitors.GetAsync() ?? [])
{
    Console.WriteLine($"{monitor.Title} {monitor.Status}");
}
```

Point it elsewhere with `new StatolyClient(token, "https://…")`.
`statoly.Api` exposes the full generated fluent API.

Generated from the Statoly OpenAPI document with Microsoft Kiota. Report issues
at [statoly/sdks](https://github.com/statoly/sdks). MIT.
