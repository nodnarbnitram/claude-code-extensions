#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "python-dotenv",
# ]
# ///
"""
Prometheus metrics queries for billing analysis.

Queries key metrics that affect billing:
- Active time series
- Samples per second (DPM)
- Storage size
- Cardinality breakdown
"""

import sys
from dataclasses import dataclass, field
from typing import Any

# Import from sibling module
from grafana_client import GrafanaClient, GrafanaClientError


@dataclass
class CardinalityEntry:
    """A single cardinality entry (metric or label with series count)."""
    name: str
    count: int


@dataclass
class PrometheusMetrics:
    """Container for Prometheus billing metrics."""
    active_series: int | None = None
    samples_per_second: float | None = None
    head_chunks: int | None = None
    storage_bytes: int | None = None
    top_metrics_by_series: list[CardinalityEntry] = field(default_factory=list)
    top_labels_by_cardinality: list[CardinalityEntry] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "active_series": self.active_series,
            "samples_per_second": self.samples_per_second,
            "data_points_per_minute": (
                round(self.samples_per_second * 60) if self.samples_per_second else None
            ),
            "head_chunks": self.head_chunks,
            "storage_bytes": self.storage_bytes,
            "top_metrics_by_series": [
                {"name": e.name, "count": e.count} for e in self.top_metrics_by_series
            ],
            "top_labels_by_cardinality": [
                {"name": e.name, "count": e.count} for e in self.top_labels_by_cardinality
            ],
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


def query_prometheus_metrics(client: GrafanaClient, limit: int = 10) -> PrometheusMetrics:
    """
    Query all Prometheus billing metrics.

    Args:
        client: Grafana client instance
        limit: Number of top cardinality entries to return

    Returns:
        PrometheusMetrics with all available data
    """
    metrics = PrometheusMetrics()

    # Find Prometheus data source
    prom_ds = client.find_datasource("prometheus")
    if not prom_ds:
        metrics.errors.append("No Prometheus data source found")
        return metrics

    ds_id = prom_ds.id

    # Query TSDB status for cardinality FIRST (most reliable)
    # AWS Managed Prometheus/Cortex/Mimir all support this endpoint
    try:
        status = client.proxy_tsdb_status(ds_id, limit=limit)
        data = status.get("data", {})

        # Top metrics by series count
        series_by_metric = data.get("seriesCountByMetricName", [])
        metrics.top_metrics_by_series = [
            CardinalityEntry(name=entry["name"], count=entry["value"])
            for entry in series_by_metric[:limit]
        ]

        # Calculate total active series from TSDB status
        # This works for AWS Managed Prometheus where prometheus_tsdb_head_series doesn't exist
        total_series = sum(entry["value"] for entry in series_by_metric)
        if total_series > 0:
            metrics.active_series = total_series

        # Top labels by cardinality
        labels_by_count = data.get("labelValueCountByLabelName", [])
        metrics.top_labels_by_cardinality = [
            CardinalityEntry(name=entry["name"], count=entry["value"])
            for entry in labels_by_count[:limit]
        ]

        # headStats contains series count in some Prometheus versions
        head_stats = data.get("headStats", {})
        if head_stats.get("numSeries") and not metrics.active_series:
            metrics.active_series = head_stats["numSeries"]
        if head_stats.get("numChunks"):
            metrics.head_chunks = head_stats["numChunks"]

    except GrafanaClientError as e:
        metrics.errors.append(f"tsdb_status: {e}")

    # Try Cortex/Mimir active series metric (AWS Managed Prometheus)
    if not metrics.active_series:
        try:
            result = client.proxy_query(ds_id, "sum(cortex_ingester_active_series)")
            value = _extract_scalar(result)
            if value and value > 0:
                metrics.active_series = int(value)
        except GrafanaClientError:
            pass  # Try next metric

    # Fallback to standard Prometheus metric
    if not metrics.active_series:
        try:
            result = client.proxy_query(ds_id, "prometheus_tsdb_head_series")
            value = _extract_scalar(result)
            if value and value > 0:
                metrics.active_series = int(value)
        except GrafanaClientError:
            pass

    # Query samples per second - try multiple metrics
    sample_rate_queries = [
        "sum(rate(cortex_ingester_ingested_samples_total[5m]))",  # Cortex/Mimir
        "sum(rate(prometheus_tsdb_head_samples_appended_total[5m]))",  # Standard Prometheus
    ]
    for query in sample_rate_queries:
        if metrics.samples_per_second:
            break
        try:
            result = client.proxy_query(ds_id, query)
            value = _extract_scalar(result)
            if value and value > 0:
                metrics.samples_per_second = value
        except GrafanaClientError:
            pass

    # Query storage size - try multiple metrics
    storage_queries = [
        "sum(cortex_ingester_tsdb_storage_blocks_bytes)",  # Cortex/Mimir
        "sum(prometheus_tsdb_storage_blocks_bytes)",  # Standard Prometheus
    ]
    for query in storage_queries:
        if metrics.storage_bytes:
            break
        try:
            result = client.proxy_query(ds_id, query)
            value = _extract_scalar(result)
            if value and value > 0:
                metrics.storage_bytes = int(value)
        except GrafanaClientError:
            pass

    return metrics


if __name__ == "__main__":
    # Test the module
    import json
    from grafana_client import get_all_clients

    clients = get_all_clients()

    for env, client in clients.items():
        print(f"\n=== {env.upper()} Prometheus Metrics ===")
        try:
            metrics = query_prometheus_metrics(client)
            print(json.dumps(metrics.to_dict(), indent=2))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
