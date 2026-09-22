# Statoly SDKs

Official clients for the [Statoly](https://statoly.com) API, in TypeScript, Python, C# and Go.

| Language | Package | Install |
|---|---|---|
| TypeScript | [`@statoly/sdk`](https://www.npmjs.com/package/@statoly/sdk) | `npm install @statoly/sdk` |
| Python | [`statoly`](https://pypi.org/project/statoly/) | `pip install statoly` |
| C# | [`Statoly.Sdk`](https://www.nuget.org/packages/Statoly.Sdk) | `dotnet add package Statoly.Sdk` |
| Go | `github.com/statoly/sdks/go` | `go get github.com/statoly/sdks/go` |

All four cover the REST API at `https://api.statoly.com/v1` and authenticate with an
organization token (`org_tok_…`) you create in the Statoly console.

## How this repository works

`openapi.json` is exported from the API and synced here by an automated pull
request whenever the REST surface changes. [Microsoft Kiota](https://github.com/microsoft/kiota)
turns it into the `generated` folder of each language, which is committed so
consumers never run a generator.

Around each generated client sits a small hand-written wrapper — the only file
you should edit — that wires the bearer token and the default base URL.

```
openapi.json  →  scripts/generate.sh  →  <language>/…/generated/  ←  hand-written wrapper
```

To regenerate after `openapi.json` changes:

```bash
dotnet tool install --global Microsoft.OpenApi.Kiota --version "$(cat .kiota-version)"
./scripts/generate.sh
```

CI regenerates and diffs, so a stale client fails the build.

## Releasing

All four SDKs share one version number. Bump it in `typescript/package.json`,
`python/pyproject.toml` and `dotnet/src/Statoly.Sdk/Statoly.Sdk.csproj`, merge,
then run the **Release** workflow with that version. It publishes to npm, PyPI
and NuGet through trusted publishing — no API keys are stored — and tags
`go/vX.Y.Z` for the Go module.

## Licence

MIT.
