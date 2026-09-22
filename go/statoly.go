// Package statoly is the official Go client for the Statoly API.
//
// Everything under ./generated is produced by Kiota from the OpenAPI document
// and must not be edited. This file is the hand-written surface: it wires the
// bearer token and the default base URL so callers never touch Kiota's
// request adapter.
package statoly

import (
	"context"
	"errors"
	"net/url"

	"github.com/microsoft/kiota-abstractions-go/authentication"
	kiotabundle "github.com/microsoft/kiota-bundle-go"

	"github.com/statoly/sdks/go/generated"
)

// DefaultBaseURL is the production API.
const DefaultBaseURL = "https://api.statoly.com/v1"

// ErrMissingToken is returned by New when no organization token is given.
var ErrMissingToken = errors.New("statoly: an organization token is required")

// Option customizes a client.
type Option func(*options)

type options struct {
	baseURL string
}

// WithBaseURL points the client at another API, such as staging or a stub.
func WithBaseURL(baseURL string) Option {
	return func(o *options) {
		o.baseURL = baseURL
	}
}

// Client talks to one Statoly organization. The embedded generated client
// carries the fluent API: client.Monitors().Get(ctx, nil).
type Client struct {
	*generated.StatolyClient
}

// New builds a client authenticating with an organization token (org_tok_…).
func New(token string, opts ...Option) (*Client, error) {
	if token == "" {
		return nil, ErrMissingToken
	}

	settings := options{baseURL: DefaultBaseURL}

	for _, apply := range opts {
		apply(&settings)
	}

	adapter, err := kiotabundle.NewDefaultRequestAdapter(
		authentication.NewBaseBearerTokenAuthenticationProvider(newStaticTokenProvider(token)),
	)
	if err != nil {
		return nil, err
	}

	adapter.SetBaseUrl(settings.baseURL)

	return &Client{StatolyClient: generated.NewStatolyClient(adapter)}, nil
}

// staticTokenProvider hands the same token to every request. Statoly issues
// long-lived organization tokens, so there is nothing to refresh. The empty
// host allow-list lets the token travel to whatever base URL the caller set,
// including a local stub in tests.
type staticTokenProvider struct {
	token     string
	validator *authentication.AllowedHostsValidator
}

func newStaticTokenProvider(token string) staticTokenProvider {
	validator := authentication.NewAllowedHostsValidator(nil)

	return staticTokenProvider{token: token, validator: &validator}
}

func (p staticTokenProvider) GetAuthorizationToken(context.Context, *url.URL, map[string]any) (string, error) {
	return p.token, nil
}

func (p staticTokenProvider) GetAllowedHostsValidator() *authentication.AllowedHostsValidator {
	return p.validator
}
