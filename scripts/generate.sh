#!/usr/bin/env bash
# Regenerates the four clients from openapi.json.
#
# The generated code is committed: consumers install a package, they do not run
# Kiota. Run this after openapi.json changes, then commit the diff.
set -euo pipefail

cd "$(dirname "$0")/.."

KIOTA_VERSION="$(cat .kiota-version)"

if ! command -v kiota >/dev/null 2>&1; then
  echo "kiota not found. Install it with:" >&2
  echo "  dotnet tool install --global Microsoft.OpenApi.Kiota --version $KIOTA_VERSION" >&2
  exit 1
fi

# Kiota's output is not stable across versions, so a mismatch here would show up
# as an unrelated diff in the generated folders.
have="$(kiota --version | cut -d+ -f1)"
if [ "$have" != "$KIOTA_VERSION" ]; then
  echo "kiota $have found, but this repository is generated with $KIOTA_VERSION." >&2
  echo "Install the pinned version or update .kiota-version deliberately." >&2
  exit 1
fi

gen() {
  local language="$1" output="$2" namespace="$3" class="${4:-StatolyClient}"
  echo "==> $language"
  kiota generate \
    --language "$language" \
    --openapi openapi.json \
    --output "$output" \
    --class-name "$class" \
    --namespace-name "$namespace" \
    --clean-output \
    --clear-cache \
    --log-level Warning
}

gen TypeScript typescript/src/generated statoly
gen Python     python/src/statoly/generated statoly.generated
# The C# wrapper is the StatolyClient consumers instantiate, so the generated
# one takes another name rather than shadowing it inside the same assembly.
gen CSharp     dotnet/src/Statoly.Sdk/Generated Statoly.Sdk.Generated StatolyApiClient
gen Go         go/generated github.com/statoly/sdks/go/generated
