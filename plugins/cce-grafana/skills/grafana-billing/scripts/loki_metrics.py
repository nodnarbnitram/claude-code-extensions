#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "python-dotenv",
# ]
# ///
"""
Loki metrics queries for billing analysis.

Queries key metrics that affect billing:
- Bytes ingested (total and rate)
- Active streams
- Memory usage (chunks)
"""

import sys
from dataclasses import dataclass, field
from typing import Any

# Import from sibling module
from grafana_client import GrafanaClient, GrafanaClientError


@dataclass
class LokiMetrics:
    """Container for Loki billing metrics."""
    bytes_received_total: int | None = None
    ingestion_rate_bytes_per_second: float | None = None
    active_streams: int | None = None
    memory_chunks: int | None = None
    rejected_bytes_total: int | None = None
    errors: list[str] = field(default_factory=list)

    @property
    def ingestion_rate_gb_per_day(self) -> float | None:
        """Calculate GB/day ingestion rate."""
        if self.ingestion_rate_bytes_per_second is None:
            return None
        # bytes/sec * 60 * 60 * 24 / (1024^3)
        return self.ingestion_rate_bytes_per_second * 86400 / (1024 ** 3)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "bytes_received_total": self.bytes_received_total,
            "ingestion_rate_bytes_per_second": self.ingestion_rate_bytes_per_second,
            "ingestion_rate_gb_per_day": (
                round(self.ingestion_rate_gb_per_day, 2)
                if self.ingestion_rate_gb_per_day else None
            ),
            "active_streams": self.active_streams,
            "memory_chunks": self.memory_chunks,
            "rejected_bytes_total": self.rejected_bytes_total,
            "errors": self.errors if self.errors else None,
        }


def _extract_scalar(result: dict[str, Any]) -> float | None:
    """Extract a scalar value from a Prometheus query result."""
    try:
        data = result.get("data", {})
        if data.get("resultType") == "vector" and data.get("result"):
            # Vector result - take first value
            value = data["result"][0]["value"][1]
            return float(value)
        elif data.get("resultType") == "scalar":
            return float(data["result"][1])
    except (IndexError, KeyError, ValueError, TypeError):
        pass
    return None


def _sum_all_values(result: dict[str, Any]) -> float | None:
    """Sum all values from a vector result."""
    try:
        data = result.get("data", {})
        if data.get("resultType") == "vector" and data.get("result"):
            total = 0.0
            for entry in data["result"]:
                total += float(entry["value"][1])
            return total
    except (IndexError, KeyError, ValueError, TypeError):
        pass
    return None


def query_loki_metrics(client: GrafanaClient) -> LokiMetrics:
    """
    Query all Loki billing metrics.

    Note: Loki metrics are typically exposed through a Prometheus data source
    that scrapes Loki's /metrics endpoint. We query these through the
    Prometheus proxy.

    Args:
        client: Grafana client instance

    Returns:
        LokiMetrics with all available data
    """
    metrics = LokiMetrics()

    # Find Prometheus data source (Loki metrics are scraped by Prometheus)
    prom_ds = client.find_datasource("prometheus")
    if not prom_ds:
        metrics.errors.append("No Prometheus data source found (needed for Loki metrics)")
        return metrics

    ds_id = prom_ds.id

    # Query total bytes received
    try:
        result = client.proxy_query(
            ds_id,
            "sum(loki_distributor_bytes_received_total)"
        )
        value = _sum_all_values(result) or _extract_scalar(result)
        metrics.bytes_received_total = int(value) if value else None
    except GrafanaClientError as e:
        metrics.errors.append(f"bytes_received_total: {e}")

    # Query ingestion rate (bytes/sec over 5m)
    try:
        result = client.proxy_query(
            ds_id,
            "sum(rate(loki_distributor_bytes_received_total[5m]))"
        )
        metrics.ingestion_rate_bytes_per_second = _extract_scalar(result)
    except GrafanaClientError as e:
        metrics.errors.append(f"ingestion_rate: {e}")

    # Query active streams
    try:
        result = client.proxy_query(
            ds_id,
            "sum(loki_ingester_memory_streams)"
        )
        value = _extract_scalar(result)
        metrics.active_streams = int(value) if value else None
    except GrafanaClientError as e:
        metrics.errors.append(f"active_streams: {e}")

    # Query memory chunks
    try:
        result = client.proxy_query(
            ds_id,
            "sum(loki_ingester_memory_chunks)"
        )
        value = _extract_scalar(result)
        metrics.memory_chunks = int(value) if value else None
    except GrafanaClientError as e:
        metrics.errors.append(f"memory_chunks: {e}")

    # Query rejected bytes (rate limiting hits)
    try:
        result = client.proxy_query(
            ds_id,
            'sum(loki_distributor_bytes_received_total{reason=~".+"})'
        )
        value = _sum_all_values(result) or _extract_scalar(result)
        metrics.rejected_bytes_total = int(value) if value else None
    except GrafanaClientError:
        # This is expected to fail if there are no rejected bytes
        pass

    return metrics


if __name__ == "__main__":
    # Test the module
    import json
    from grafana_client import get_all_clients

    clients = get_all_clients()

    for env, client in clients.items():
        print(f"\n=== {env.upper()} Loki Metrics ===")
        try:
            metrics = query_loki_metrics(client)
            print(json.dumps(metrics.to_dict(), indent=2))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
