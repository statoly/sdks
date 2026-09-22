using System.Net;
using System.Net.Sockets;
using System.Text;
using Xunit;

namespace Statoly.Sdk.Tests;

public class StatolyClientTests
{
    private const string MonitorsBody = """
    [{
      "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
      "title": "Homepage",
      "type": "http",
      "status": "up",
      "active": true,
      "metadata": [{ "key": "team", "value": "platform" }],
      "createdAt": "2026-01-02T03:04:05Z",
      "updatedAt": "2026-01-02T03:05:05Z"
    }]
    """;

    [Fact]
    public async Task SendsBearerTokenAndParsesResponse()
    {
        using var stub = new Stub(MonitorsBody);

        var statoly = new StatolyClient("org_tok_test", stub.BaseUrl);

        var monitors = await statoly.Monitors.GetAsync();

        Assert.Equal("Bearer org_tok_test", stub.LastAuthorization);
        Assert.Equal("/monitors", stub.LastPath);

        var monitor = Assert.Single(monitors!);
        Assert.Equal(Guid.Parse("6ba7b810-9dad-11d1-80b4-00c04fd430c8"), monitor.Id);
        Assert.Equal("Homepage", monitor.Title);
        // The spec says date-time, so the client must hand back a parsed instant
        // rather than the raw string. This is what the DTO layer guarantees.
        Assert.Equal(2026, monitor.CreatedAt!.Value.Year);
        Assert.Equal("team", monitor.Metadata![0].Key);
    }

    [Fact]
    public void RefusesAnEmptyToken()
    {
        Assert.Throws<ArgumentException>(() => new StatolyClient(""));
    }

    /// <summary>Minimal HTTP server answering every request with one canned body.</summary>
    private sealed class Stub : IDisposable
    {
        private readonly HttpListener listener = new();

        public string BaseUrl { get; }
        public string? LastAuthorization { get; private set; }
        public string? LastPath { get; private set; }

        public Stub(string body)
        {
            var probe = new TcpListener(IPAddress.Loopback, 0);
            probe.Start();
            var port = ((IPEndPoint)probe.LocalEndpoint).Port;
            probe.Stop();

            BaseUrl = $"http://127.0.0.1:{port}";
            listener.Prefixes.Add($"{BaseUrl}/");
            listener.Start();

            _ = Task.Run(async () =>
            {
                while (listener.IsListening)
                {
                    HttpListenerContext context;

                    try
                    {
                        context = await listener.GetContextAsync();
                    }
                    catch (Exception)
                    {
                        return;
                    }

                    LastAuthorization = context.Request.Headers["Authorization"];
                    LastPath = context.Request.Url?.AbsolutePath;

                    var payload = Encoding.UTF8.GetBytes(body);
                    context.Response.ContentType = "application/json";
                    context.Response.ContentLength64 = payload.Length;
                    await context.Response.OutputStream.WriteAsync(payload);
                    context.Response.Close();
                }
            });
        }

        public void Dispose() => listener.Close();
    }
}
