package statoly

import (
	"context"
	"net/http"
	"net/http/httptest"
	"testing"
)

const monitorsBody = `[{
  "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "title": "Homepage",
  "type": "http",
  "status": "up",
  "active": true,
  "metadata": [{"key": "team", "value": "platform"}],
  "createdAt": "2026-01-02T03:04:05Z",
  "updatedAt": "2026-01-02T03:05:05Z"
}]`

func TestClientSendsBearerTokenAndParsesMonitors(t *testing.T) {
	var gotAuth, gotPath string

	stub := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		gotAuth = r.Header.Get("Authorization")
		gotPath = r.URL.Path

		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(monitorsBody))
	}))
	defer stub.Close()

	client, err := New("org_tok_test", WithBaseURL(stub.URL))
	if err != nil {
		t.Fatal(err)
	}

	monitors, err := client.Monitors().Get(context.Background(), nil)
	if err != nil {
		t.Fatal(err)
	}

	if gotAuth != "Bearer org_tok_test" {
		t.Errorf("Authorization = %q, want the token as a bearer credential", gotAuth)
	}

	if gotPath != "/monitors" {
		t.Errorf("path = %q, want /monitors", gotPath)
	}

	if len(monitors) != 1 {
		t.Fatalf("got %d monitors, want 1", len(monitors))
	}

	if id := monitors[0].GetId(); id == nil || id.String() != "6ba7b810-9dad-11d1-80b4-00c04fd430c8" {
		t.Errorf("id = %v, want the uuid from the response", id)
	}

	// The spec says date-time, so the client must hand back a time.Time rather
	// than the raw string. This is what the DTO layer exists to guarantee.
	if created := monitors[0].GetCreatedAt(); created == nil || created.Year() != 2026 {
		t.Errorf("createdAt = %v, want the parsed instant", created)
	}
}

func TestNewRefusesAnEmptyToken(t *testing.T) {
	if _, err := New(""); err != ErrMissingToken {
		t.Errorf("err = %v, want ErrMissingToken", err)
	}
}
