"""Simplified GraphQL client."""

import asyncio
from typing import Any, Dict, Optional

from gql import Client, gql
from gql.client import AsyncClientSession, GraphQLRequest
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportError

from my_app.core.logger import get_logger

log = get_logger(__name__)


class GraphQLClient:
    """Simplified GraphQL client for querying and mutations."""

    def __init__(
        self,
        http_endpoint: str,
        token_id: str,
        token_value: str,
        timeout: int = 30,
    ):
        self.http_endpoint = http_endpoint
        self.timeout = timeout

        self._auth_headers = {
            "Authorization": f"Bearer {token_value}",
            "x-token-id": token_id,
            "x-token-value": token_value,
        }

        self._transport: Optional[AIOHTTPTransport] = None
        self._client: Optional[Client] = None
        self._session: Optional[AsyncClientSession] = None
        log.info(f"GraphQL client initialized for endpoint: {http_endpoint}")

    async def start(self) -> None:
        """Initialize the GraphQL client and open a persistent session."""
        try:
            self._transport = AIOHTTPTransport(
                url=self.http_endpoint,
                headers=self._auth_headers,
                timeout=self.timeout,
            )

            self._client = Client(
                transport=self._transport,
                fetch_schema_from_transport=False,
            )

            self._session = await self._client.connect_async(reconnecting=False)
            log.info("GraphQL client started successfully")
        except Exception as e:
            log.error(f"Failed to start GraphQL client: {e}")
            raise

    async def close(self) -> None:
        """Close the GraphQL client session."""
        try:
            if self._session is not None and self._client is not None:
                await self._client.close_async()
            self._session = None
            self._client = None
            self._transport = None
            log.info("GraphQL client closed")
        except Exception as e:
            log.error(f"Error closing GraphQL client: {e}")

    async def query(
        self,
        query_str: str,
        variables: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        """Execute a GraphQL query."""
        if not self._session:
            raise RuntimeError("Client not started. Call start() first.")

        for attempt in range(max_retries):
            try:
                query = gql(query_str)
                request = GraphQLRequest(query, variable_values=variables)
                result = await self._session.execute(request)
                return result
            except TransportError as e:
                log.warning(f"Query attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt == max_retries - 1:
                    log.error(f"Query failed after {max_retries} attempts")
                    raise
                await asyncio.sleep(min(2 ** attempt, 5))
            except Exception as e:
                log.error(f"Unexpected error during query: {e}")
                raise

        raise RuntimeError("Query failed")

    async def mutate(
        self,
        mutation_str: str,
        variables: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        """Execute a GraphQL mutation."""
        if not self._session:
            raise RuntimeError("Client not started. Call start() first.")

        for attempt in range(max_retries):
            try:
                mutation = gql(mutation_str)
                request = GraphQLRequest(mutation, variable_values=variables)
                result = await self._session.execute(request)
                return result
            except TransportError as e:
                log.warning(f"Mutation attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt == max_retries - 1:
                    log.error(f"Mutation failed after {max_retries} attempts")
                    raise
                await asyncio.sleep(min(2 ** attempt, 5))
            except Exception as e:
                log.error(f"Unexpected error during mutation: {e}")
                raise

        raise RuntimeError("Mutation failed")

    async def __aenter__(self) -> "GraphQLClient":
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()
