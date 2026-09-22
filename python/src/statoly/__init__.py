"""Official Python client for the Statoly API.

Everything under ``statoly.generated`` is produced by Kiota from the OpenAPI
document and must not be edited. This module is the hand-written surface: it
wires the bearer token and the default base URL so callers never touch Kiota's
request adapter.
"""

from __future__ import annotations

from typing import Any, Optional
from urllib.parse import urlparse

from kiota_abstractions.authentication import (
    AccessTokenProvider,
    AllowedHostsValidator,
    BaseBearerTokenAuthenticationProvider,
)
from kiota_bundle.default_request_adapter import DefaultRequestAdapter

from .generated.statoly_client import StatolyClient

#: Base URL of the production API.
DEFAULT_BASE_URL = "https://api.statoly.com/v1"

__all__ = ["DEFAULT_BASE_URL", "Statoly", "StatolyClient"]


class _StaticTokenProvider(AccessTokenProvider):
    """Hands the same token to every request.

    Statoly issues long-lived organization tokens (``org_tok_…``), so there is
    nothing to refresh. The empty host allow-list lets the token travel to
    whatever base URL the caller configured, including a local stub in tests.
    """

    def __init__(self, token: str) -> None:
        self._token = token
        self._validator = AllowedHostsValidator([])

    async def get_authorization_token(
        self, uri: str, additional_authentication_context: dict[str, Any] = {}
    ) -> str:
        return self._token

    def get_allowed_hosts_validator(self) -> AllowedHostsValidator:
        return self._validator


class Statoly:
    """A client for one Statoly organization.

    ::

        statoly = Statoly(os.environ["STATOLY_TOKEN"])
        monitors = await statoly.monitors.get()
    """

    def __init__(self, token: str, base_url: Optional[str] = None) -> None:
        if not token:
            raise ValueError("Statoly: an organization token is required")

        adapter = DefaultRequestAdapter(
            BaseBearerTokenAuthenticationProvider(_StaticTokenProvider(token))
        )
        adapter.base_url = base_url or DEFAULT_BASE_URL

        #: The generated fluent API, for anything this wrapper does not surface.
        self.api = StatolyClient(adapter)

    @property
    def monitors(self):
        """``/monitors`` and everything below it."""
        return self.api.monitors
