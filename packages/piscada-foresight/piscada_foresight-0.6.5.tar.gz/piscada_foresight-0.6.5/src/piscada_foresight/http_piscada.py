"""Authenticated HTTPXTransport used to connect to Foresight.

This module provides a transport class for connecting to Foresight's GraphQL API using
OAuth2 authentication. It handles token management, automatic refresh, and interactive
browser-based login when needed.

The main class is ForesightHTTPXTransport which can be used with the gql library
to make authenticated GraphQL requests.
"""

import http.server
import json
import logging
import socket
import socketserver
import webbrowser
from contextlib import closing
from pathlib import Path
from typing import Any, Callable

import httpx
from authlib.common.security import generate_token
from authlib.integrations.httpx_client import OAuth2Client, OAuthError
from authlib.oauth2.rfc7636 import create_s256_code_challenge
from gql.transport.exceptions import TransportAlreadyConnected
from gql.transport.httpx import HTTPXTransport

SCOPE = "email"
CODE_CHALLENGE_METHOD = "S256"

log = logging.getLogger(__name__)


def _find_free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def _get_config(domain: str) -> dict:
    config_response = httpx.get(
        f"https://accounts.{domain}/realms/foresight/.well-known/openid-configuration",
        timeout=10.0,
    )
    if config_response.status_code != httpx.codes.OK:
        msg = f"Could not fetch authentication configuration from {domain}."
        raise RuntimeError(
            msg,
        )
    return config_response.json()


def _get_state_file(client_id: str) -> Path:
    return Path().home() / Path(f".{client_id}_state")


def _has_state_and_refresh_token(domain: str, client_id: str) -> bool:
    try:
        persisted_state = json.load(_get_state_file(client_id).open())
    except FileNotFoundError:
        return False
    return (
        domain in persisted_state
        and "state" in persisted_state[domain]
        and "refresh_token" in persisted_state[domain]
    )


def _get_state_and_refresh_token(domain: str, client_id: str) -> tuple[str, str]:
    persisted_state = json.load(_get_state_file(client_id).open())
    state = persisted_state[domain]["state"]
    refresh_token = persisted_state[domain]["refresh_token"]
    return (state, refresh_token)


def _save_state_and_refresh_token(
    domain: str, client_id: str, state: str, refresh_token: str,
) -> None:
    json.dump(
        {domain: {"state": state, "refresh_token": refresh_token}},
        _get_state_file(client_id).open("w"),
    )


def _get_interactive_client(domain: str,
                            client_id: str,
                            **kwargs: object,
                            ) -> OAuth2Client:
    port = _find_free_port()
    openid_configuration = _get_config(domain)
    if _has_state_and_refresh_token(domain, client_id):
        state, refresh_token = _get_state_and_refresh_token(domain, client_id)
        client = OAuth2Client(
            client_id,
            scope=SCOPE,
            code_challenge_method=CODE_CHALLENGE_METHOD,
            state=state,
            **kwargs,
        )
        try:
            token = client.refresh_token(
                openid_configuration["token_endpoint"], refresh_token=refresh_token,
            )
            _save_state_and_refresh_token(
                domain, client_id, state, token["refresh_token"],
            )
        except OAuthError:
            _get_state_file(client_id).unlink(missing_ok=True)
            return _get_interactive_client(domain, client_id, **kwargs)
        else:
            return client
    # We need to fetch a new token from scratch.
    code_verifier = generate_token(48)
    code_challenge = create_s256_code_challenge(code_verifier)

    client = OAuth2Client(
        client_id=client_id,
        redirect_uri=f"http://localhost:{port}/callback",
        code_verifier=code_verifier,
        **kwargs,
    )

    uri, state = client.create_authorization_url(
        openid_configuration["authorization_endpoint"],
        scope=SCOPE,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )

    class CallbackHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self) -> None: # noqa: N802
            if self.path.startswith("/callback"):
                authorization_response = self.path

                token = client.fetch_token(
                    openid_configuration["token_endpoint"],
                    authorization_response=authorization_response,
                    code_verifier=code_verifier,
                )
                _save_state_and_refresh_token(
                    domain, client_id, state, token["refresh_token"],
                )

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"Authorization complete. You can close this window.")
            else:
                self.send_error(404)
                msg = "Could not retrieve response."
                raise RuntimeError(msg)

    with socketserver.TCPServer(("localhost", port), CallbackHandler) as httpd:
        webbrowser.open(uri)
        httpd.handle_request()

    return client


def _get_non_interactive_client(
    domain: str, client_id: str, client_secret: str, **kwargs: object,
) -> OAuth2Client:
    """Create an OAuth2Client using client credentials flow.

    Args:
        domain: The Foresight domain to authenticate against
        client_id: OAuth2 client ID
        client_secret: OAuth2 client secret
        **kwargs: Additional arguments passed to OAuth2Client

    Returns:
        OAuth2Client configured with access token

    """
    openid_configuration = _get_config(domain)

    client = OAuth2Client(
        client_id=client_id, client_secret=client_secret, scope=SCOPE, **kwargs,
    )

    client.fetch_token(
        openid_configuration["token_endpoint"], grant_type="client_credentials",
    )

    return client


class ForesightHTTPXTransport(HTTPXTransport):
    """Sync HTTPXTransport using OAuth2 authentication with Foresight.

    This transport handles OAuth2 authentication flow with Foresight, including
    automatic token refresh and browser-based login when needed. It manages state
    and refresh tokens persistently between sessions.

    Examples:
        transport = ForesightHTTPXTransport(
            domain="foresight.example.com",
            client_id="my-client"
        )
        client = Client(transport=transport)

    """

    def __init__(
            self,
            domain: str,
            client_id: str | None = "foresight-lib-py",
            client_secret: str | None = None,
            graphql_endpoint: str | None = None,
            json_serialize: Callable[[Any], str] = json.dumps,
            **kwargs: object,
    ) -> None:
        """Create a new ForesightHTTPXTransport.

        Uses 'Authorization Code Flow with Proof Key for Code Exchange (PKCE)',
        when only client_id is given (default). Set client_id and client_secret to use
        Client Credentials Flow.
        Put both client_id and client_secret (=None) to disable auth.

        Parameters
        ----------
        domain : str
            Which Foresight domain to authenticate against.
        client_id : str, optional
            The OAuth2 client ID to use for authentication. Defaults:"foresight-lib-py".
        client_secret : str, optional
            The OAuth2 client secret to use for authentication. Defaults to "None".
        graphql_endpoint : str, optional
            The GraphQL endpoint URL. If not provided, defaults to "https://graphql.{domain}/".
        json_serialize : callable, optional
            Function to serialize JSON data, by default json.dumps.
        **kwargs : dict
            Additional arguments passed to the underlying OAuth2Client.

        """
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        if graphql_endpoint:
            super().__init__(graphql_endpoint, json_serialize, **kwargs)
        else:
            super().__init__(f"https://graphql.{domain}/", json_serialize, **kwargs)

    def connect(self) -> None:
        """Instantiate a new authenticated client connection.

        This method handles the OAuth2 authentication flow, including automatic
        token refresh and browser-based login when needed.

        Raises
        ------
        TransportAlreadyConnected
            If a client connection has already been established.
        RuntimeError
            If authentication fails or the response cannot be retrieved.

        """
        if self.client:
            msg = "Transport is already connected"
            raise TransportAlreadyConnected(msg)

        log.debug("Connecting transport")

        if self.client_id and not self.client_secret:
            self.client = _get_interactive_client(
                self.domain, self.client_id, **self.kwargs,
            )
        elif self.client_id and self.client_secret:
            self.client = _get_non_interactive_client(
                self.domain, self.client_id, self.client_secret, **self.kwargs,
            )
        elif not self.client_id and not self.client_secret:
            self.client = httpx.Client(**self.kwargs)
