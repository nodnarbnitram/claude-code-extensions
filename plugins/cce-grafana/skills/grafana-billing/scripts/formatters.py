#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "rich",
# ]
# ///
"""
Output formatters for billing metrics.

Provides both human-readable table output and JSON serialization.
"""

import json
from typing import Any

from rich.console import Console
from rich.table import Table


def format_bytes(value: int | float | None) -> str:
    """Format bytes as human-readable string."""
    if value is None:
        return "N/A"

    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    return f"{size:.2f} {units[unit_index]}"


def format_number(value: int | float | None) -> str:
    """Format large numbers with commas."""
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:,.2f}"
    return f"{value:,}"


def format_rate(value: float | None, unit: str = "/sec") -> str:
    """Format a rate value."""
    if value is None:
        return "N/A"
    return f"{format_number(value)}{unit}"


def print_prometheus_metrics(env: str, metrics: dict[str, Any], console: Console) -> None:
    """Print Prometheus metrics as a formatted table."""
    table = Table(title="Prometheus Metrics", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="dim")
    table.add_column("Value", justify="right")
    table.add_column("Notes", style="dim")

    # Active series
    active = metrics.get("active_series")
    table.add_row(
        "Active Time Series",
        format_number(active),
        "Primary billing metric"
    )

    # Samples per second / DPM
    sps = metrics.get("samples_per_second")
    dpm = metrics.get("data_points_per_minute")
    table.add_row(
        "Samples/sec",
        format_rate(sps),
        f"DPM: {format_number(dpm)}" if dpm else ""
    )

    # Head chunks
    chunks = metrics.get("head_chunks")
    table.add_row("Head Chunks", format_number(chunks), "Memory indicator")

    # Storage
    storage = metrics.get("storage_bytes")
    table.add_row("TSDB Storage", format_bytes(storage), "On-disk size")

    console.print(table)

    # Top cardinality
    top_metrics = metrics.get("top_metrics_by_series", [])
    if top_metrics:
        card_table = Table(title="Top Metrics by Series Count", show_header=True)
        card_table.add_column("#", style="dim", width=3)
        card_table.add_column("Metric Name")
        card_table.add_column("Series", justify="right")

        for i, entry in enumerate(top_metrics[:10], 1):
            card_table.add_row(
                str(i),
                entry["name"],
                format_number(entry["count"])
            )

        console.print(card_table)

    # Errors
    errors = metrics.get("errors")
    if errors:
        console.print(f"[yellow]Warnings: {', '.join(errors)}[/yellow]")


def print_loki_metrics(env: str, metrics: dict[str, Any], console: Console) -> None:
    """Print Loki metrics as a formatted table."""
    table = Table(title="Loki Metrics", show_header=True, header_style="bold green")
    table.add_column("Metric", style="dim")
    table.add_column("Value", justify="right")
    table.add_column("Notes", style="dim")

    # Ingestion rate
    gb_day = metrics.get("ingestion_rate_gb_per_day")
    bytes_sec = metrics.get("ingestion_rate_bytes_per_second")
    table.add_row(
        "Ingestion Rate",
        f"{gb_day:.2f} GB/day" if gb_day else "N/A",
        f"({format_bytes(bytes_sec)}/sec)" if bytes_sec else ""
    )

    # Total bytes
    total = metrics.get("bytes_received_total")
    table.add_row("Total Bytes Received", format_bytes(total), "Cumulative")

    # Active streams
    streams = metrics.get("active_streams")
    table.add_row("Active Streams", format_number(streams), "")

    # Memory chunks
    chunks = metrics.get("memory_chunks")
    table.add_row("Memory Chunks", format_number(chunks), "")

    # Rejected bytes
    rejected = metrics.get("rejected_bytes_total")
    if rejected and rejected > 0:
        table.add_row(
            "Rejected Bytes",
            format_bytes(rejected),
            "[red]Rate limiting[/red]"
        )

    console.print(table)

    # Errors
    errors = metrics.get("errors")
    if errors:
        console.print(f"[yellow]Warnings: {', '.join(errors)}[/yellow]")


def print_environment_header(env: str, console: Console) -> None:
    """Print an environment header."""
    console.print()
    console.rule(f"[bold]{env.upper()} Environment[/bold]", style="blue")
    console.print()


def print_all_metrics(
    results: dict[str, dict[str, Any]],
    console: Console | None = None
) -> None:
    """
    Print all metrics for all environments.

    Args:
        results: Dict mapping env -> {"prometheus": ..., "loki": ...}
        console: Rich console (created if not provided)
    """
    if console is None:
        console = Console()

    for env, data in results.items():
        print_environment_header(env, console)

        if "prometheus" in data:
            print_prometheus_metrics(env, data["prometheus"], console)
            console.print()

        if "loki" in data:
            print_loki_metrics(env, data["loki"], console)
            console.print()


def format_json(results: dict[str, dict[str, Any]], pretty: bool = True) -> str:
    """Format results as JSON string."""
    # Remove None values for cleaner output
    cleaned = {}
    for env, data in results.items():
        cleaned[env] = {}
        for service, metrics in data.items():
            if metrics:
                # Remove None and empty list values
                cleaned_metrics = {
                    k: v for k, v in metrics.items()
                    if v is not None and v != []
                }
                cleaned[env][service] = cleaned_metrics

    if pretty:
        return json.dumps(cleaned, indent=2)
    return json.dumps(cleaned)


if __name__ == "__main__":
    # Demo the formatters
    console = Console()

    sample_results = {
        "staging": {
            "prometheus": {
                "active_series": 1234567,
                "samples_per_second": 45678.9,
                "data_points_per_minute": 2740734,
                "head_chunks": 2500000,
                "storage_bytes": 13421772800,
                "top_metrics_by_series": [
                    {"name": "http_requests_total", "count": 125000},
                    {"name": "container_cpu_usage", "count": 98000},
                    {"name": "node_memory_bytes", "count": 45000},
                ],
                "errors": None,
            },
            "loki": {
                "bytes_received_total": 1234567890123,
                "ingestion_rate_bytes_per_second": 28571.43,
                "ingestion_rate_gb_per_day": 2.3,
                "active_streams": 5432,
                "memory_chunks": 12000,
                "errors": None,
            },
        }
    }

    print_all_metrics(sample_results, console)
    console.print("\n[dim]JSON output:[/dim]")
    console.print(format_json(sample_results))
