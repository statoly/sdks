using Microsoft.Kiota.Abstractions.Authentication;
using Microsoft.Kiota.Bundle;
using Statoly.Sdk.Generated;
using Statoly.Sdk.Generated.Monitors;

namespace Statoly.Sdk;

/// <summary>
/// A client for one Statoly organization.
/// </summary>
/// <remarks>
/// Everything under <c>Statoly.Sdk.Generated</c> is produced by Kiota from the
/// OpenAPI document and must not be edited. This class is the hand-written
/// surface: it wires the bearer token and the default base URL so callers never
/// touch Kiota's request adapter.
/// <code>
/// var statoly = new StatolyClient(Environment.GetEnvironmentVariable("STATOLY_TOKEN")!);
/// var monitors = await statoly.Monitors.GetAsync();
/// </code>
/// </remarks>
public sealed class StatolyClient
{
    /// <summary>Base URL of the production API.</summary>
    public const string DefaultBaseUrl = "https://api.statoly.ch/v1";

    /// <summary>The generated fluent API, for anything this wrapper does not surface.</summary>
    public StatolyApiClient Api { get; }

    /// <param name="token">An organization token (<c>org_tok_…</c>).</param>
    /// <param name="baseUrl">Overrides the API the client talks to. Useful for staging.</param>
    public StatolyClient(string token, string? baseUrl = null)
    {
        if (string.IsNullOrEmpty(token))
        {
            throw new ArgumentException("An organization token is required", nameof(token));
        }

        var adapter = new DefaultRequestAdapter(
            new BaseBearerTokenAuthenticationProvider(new StaticTokenProvider(token)));

        adapter.BaseUrl = baseUrl ?? DefaultBaseUrl;

        Api = new StatolyApiClient(adapter);
    }

    /// <summary><c>/monitors</c> and everything below it.</summary>
    public MonitorsRequestBuilder Monitors => Api.Monitors;
}

/// <summary>
/// Hands the same token to every request. Statoly issues long-lived
/// organization tokens, so there is nothing to refresh. The empty host
/// allow-list lets the token travel to whatever base URL the caller set,
/// including a local stub in tests.
/// </summary>
internal sealed class StaticTokenProvider(string token) : IAccessTokenProvider
{
    public AllowedHostsValidator AllowedHostsValidator { get; } = new();

    public Task<string> GetAuthorizationTokenAsync(
        Uri uri,
        Dictionary<string, object>? additionalAuthenticationContext = null,
        CancellationToken cancellationToken = default) => Task.FromResult(token);
}
