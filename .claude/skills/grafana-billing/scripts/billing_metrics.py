#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "python-dotenv",
#     "rich",
# ]
# ///
"""
Grafana Billing Metrics CLI

Query key billing metrics from Prometheus and Loki through Grafana's
data source proxy API.

Usage:
    # Query both environments (default)
    uv run billing_metrics.py

    # Query specific environment
    uv run billing_metrics.py --env staging
    uv run billing_metrics.py --env prod

    # JSON output for automation
    uv run billing_metrics.py --json

    # Filter to specific service
    uv run billing_metrics.py --service prometheus
    uv run billing_metrics.py --service loki

Environment Variables:
    GRAFANA_STAGING_API_KEY - API key for staging Grafana
    GRAFANA_PROD_API_KEY - API key for prod Grafana
"""

import argparse
import sys
from pathlib import Path

# Add scripts directory to path for sibling imports
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console

from grafana_client import GrafanaClient, GrafanaClientError, ENVIRONMENTS
from prometheus_metrics import query_prometheus_metrics
from loki_metrics import query_loki_metrics
from formatters import print_all_metrics, format_json


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Query Grafana billing metrics from Prometheus and Loki",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "--env",
        choices=list(ENVIRONMENTS.keys()),
        help="Environment to query (default: all)"
    )

    parser.add_argument(
        "--service",
        choices=["prometheus", "loki"],
        help="Service to query (default: all)"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results as JSON"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of top cardinality entries to show (default: 10)"
    )

    return parser.parse_args()


def query_environment(
    env: str,
    service_filter: str | None = None,
    cardinality_limit: int = 10
) -> dict:
    """
    Query all metrics for a single environment.

    Args:
        env: Environment name
        service_filter: Optional filter for 'prometheus' or 'loki'
        cardinality_limit: Number of top cardinality entries

    Returns:
        Dict with prometheus and/or loki metrics
    """
    results = {}

    try:
        client = GrafanaClient(env)
    except GrafanaClientError as e:
        return {"error": str(e)}

    # Query Prometheus
    if service_filter is None or service_filter == "prometheus":
        try:
            prom_metrics = query_prometheus_metrics(client, limit=cardinality_limit)
            results["prometheus"] = prom_metrics.to_dict()
        except Exception as e:
            results["prometheus"] = {"error": str(e)}

    # Query Loki
    if service_filter is None or service_filter == "loki":
        try:
            loki_metrics = query_loki_metrics(client)
            results["loki"] = loki_metrics.to_dict()
        except Exception as e:
            results["loki"] = {"error": str(e)}

    return results


def main() -> int:
    """Main entry point."""
    args = parse_args()
    console = Console(stderr=True)

    # Determine which environments to query
    if args.env:
        envs_to_query = [args.env]
    else:
        envs_to_query = list(ENVIRONMENTS.keys())

    # Query all environments
    all_results = {}
    errors = []

    for env in envs_to_query:
        if not args.json_output:
            console.print(f"[dim]Querying {env}...[/dim]", highlight=False)

        result = query_environment(
            env,
            service_filter=args.service,
            cardinality_limit=args.limit
        )

        if "error" in result:
            errors.append(f"{env}: {result['error']}")
        else:
            all_results[env] = result

    # Handle case where all environments failed
    if not all_results:
        console.print("[red]Error: Could not query any environments[/red]")
        for error in errors:
            console.print(f"  [yellow]{error}[/yellow]")
        return 1

    # Output results
    if args.json_output:
        print(format_json(all_results))
    else:
        output_console = Console()
        print_all_metrics(all_results, output_console)

        # Print any errors that occurred
        if errors:
            console.print()
            for error in errors:
                console.print(f"[yellow]Warning: {error}[/yellow]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
