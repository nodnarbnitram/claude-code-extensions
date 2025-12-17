#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "python-dotenv",
# ]
# ///
"""
Grafana API Client for querying metrics through data source proxy.

Supports querying Prometheus and Loki data sources through Grafana's
authenticated proxy API, avoiding the need for direct access to the
underlying data stores.
"""

import os
import sys
import time as time_module
from dataclasses import dataclass
from typing import Any

import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment configurations
ENVIRONMENTS = {
    "staging": {
        "url": "https://g-36d2ad532d.grafana-workspace.us-east-1.amazonaws.com",
        "api_key_env": "GRAFANA_STAGING_API_KEY",
    },
    "prod": {
        "url": "https://g-d7b664d183.grafana-workspace.us-east-1.amazonaws.com",
        "api_key_env": "GRAFANA_PROD_API_KEY",
    },
}


@dataclass
class DataSource:
    """Represents a Grafana data source."""
    id: int
    uid: str
    name: str
    type: str
    url: str


class GrafanaClientError(Exception):
    """Base exception for Grafana client errors."""
    pass


class GrafanaClient:
    """Client for interacting with Grafana HTTP API."""

    def __init__(self, env: str, timeout: float = 30.0):
        """
        Initialize Grafana client for a specific environment.

        Args:
            env: Environment name ('staging' or 'prod')
            timeout: Request timeout in seconds
        """
        if env not in ENVIRONMENTS:
            raise ValueError(f"Unknown environment: {env}. Must be one of {list(ENVIRONMENTS.keys())}")

        config = ENVIRONMENTS[env]
        self.env = env
        self.base_url = config["url"]
        self.timeout = timeout

        api_key = os.getenv(config["api_key_env"])
        if not api_key:
            raise GrafanaClientError(
                f"Missing API key for {env}. Set {config['api_key_env']} environment variable."
            )

        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        self._datasources_cache: dict[str, DataSource] | None = None

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        """Make an HTTP request to Grafana API."""
        url = f"{self.base_url}{path}"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.request(
                    method,
                    url,
                    headers=self.headers,
                    **kwargs
                )
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            raise GrafanaClientError(f"Request timed out: {url}")
        except httpx.HTTPStatusError as e:
            raise GrafanaClientError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise GrafanaClientError(f"Request failed: {e}")

    def get_datasources(self) -> list[DataSource]:
        """Get all configured data sources."""
        if self._datasources_cache is not None:
            return list(self._datasources_cache.values())

        data = self._request("GET", "/api/datasources")
        datasources = [
            DataSource(
                id=ds["id"],
                uid=ds["uid"],
                name=ds["name"],
                type=ds["type"],
                url=ds.get("url", ""),
            )
            for ds in data
        ]

        self._datasources_cache = {ds.type: ds for ds in datasources}
        return datasources

    def find_datasource(self, ds_type: str) -> DataSource | None:
        """Find a data source by type (e.g., 'prometheus', 'loki')."""
        if self._datasources_cache is None:
            self.get_datasources()

        return self._datasources_cache.get(ds_type)

    def proxy_query(self, datasource_id: int, query: str, time: float | None = None) -> dict[str, Any]:
        """
        Execute a PromQL query through Grafana's data source proxy.

        Args:
            datasource_id: The data source ID
            query: PromQL query string
            time: Evaluation time as Unix timestamp (default: current time)

        Returns:
            Query result from Prometheus API
        """
        if time is None:
            time = time_module.time()
        path = f"/api/datasources/proxy/{datasource_id}/api/v1/query"
        return self._request("GET", path, params={"query": query, "time": str(time)})

    def proxy_query_range(
        self,
        datasource_id: int,
        query: str,
        start: str,
        end: str,
        step: str = "60s"
    ) -> dict[str, Any]:
        """
        Execute a range query through Grafana's data source proxy.

        Args:
            datasource_id: The data source ID
            query: PromQL query string
            start: Start time (e.g., 'now-1h')
            end: End time (e.g., 'now')
            step: Query resolution step

        Returns:
            Query result from Prometheus API
        """
        path = f"/api/datasources/proxy/{datasource_id}/api/v1/query_range"
        return self._request(
            "GET",
            path,
            params={"query": query, "start": start, "end": end, "step": step}
        )

    def proxy_tsdb_status(self, datasource_id: int, limit: int = 10) -> dict[str, Any]:
        """
        Get TSDB status (cardinality info) through Grafana's data source proxy.

        Args:
            datasource_id: The data source ID
            limit: Number of top series to return

        Returns:
            TSDB status from Prometheus API
        """
        path = f"/api/datasources/proxy/{datasource_id}/api/v1/status/tsdb"
        return self._request("GET", path, params={"limit": limit})

    def proxy_labels(self, datasource_id: int) -> dict[str, Any]:
        """Get all label names from the data source."""
        path = f"/api/datasources/proxy/{datasource_id}/api/v1/labels"
        return self._request("GET", path)


def get_client(env: str) -> GrafanaClient:
    """
    Factory function to create a Grafana client for an environment.

    Args:
        env: Environment name ('staging' or 'prod')

    Returns:
        Configured GrafanaClient instance
    """
    return GrafanaClient(env)


def get_all_clients() -> dict[str, GrafanaClient]:
    """
    Create clients for all available environments.

    Returns:
        Dict mapping environment name to client
    """
    clients = {}
    errors = []

    for env in ENVIRONMENTS:
        try:
            clients[env] = GrafanaClient(env)
        except GrafanaClientError as e:
            errors.append(f"{env}: {e}")

    if errors and not clients:
        raise GrafanaClientError("No environments available:\n" + "\n".join(errors))

    return clients


if __name__ == "__main__":
    # Test the client
    for env in ENVIRONMENTS:
        print(f"\n=== Testing {env} ===")
        try:
            client = GrafanaClient(env)
            datasources = client.get_datasources()
            print(f"Found {len(datasources)} data sources:")
            for ds in datasources:
                print(f"  - {ds.name} ({ds.type})")
        except GrafanaClientError as e:
            print(f"Error: {e}", file=sys.stderr)
