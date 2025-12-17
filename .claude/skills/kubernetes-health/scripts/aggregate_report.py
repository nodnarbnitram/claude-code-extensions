#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Health Report Aggregation Script

Aggregates results from multiple health check agents into a unified report.
Calculates weighted scores and determines overall health status.

Usage:
    uv run aggregate_report.py [--reports-dir PATH] [--output summary|detailed|json]
    cat reports/*.json | uv run aggregate_report.py
"""

import json
import sys
from datetime import datetime, timezone
from typing import Any


# Component weights for overall score calculation
COMPONENT_WEIGHTS = {
    "Core": 1.0,  # Core is always weighted highest
    "default": 0.8,  # Operators weighted slightly lower
}

# Check category weights
CHECK_WEIGHTS = {
    "availability": 0.40,
    "configuration": 0.25,
    "freshness": 0.20,
    "resources": 0.15,
}

# Status thresholds
STATUS_THRESHOLDS = {
    "HEALTHY": 90,
    "DEGRADED": 60,
    "CRITICAL": 0,
}


def determine_status(score: float) -> str:
    """Determine health status from score."""
    if score >= STATUS_THRESHOLDS["HEALTHY"]:
        return "HEALTHY"
    elif score >= STATUS_THRESHOLDS["DEGRADED"]:
        return "DEGRADED"
    else:
        return "CRITICAL"


def calculate_component_score(checks: list[dict[str, Any]]) -> float:
    """Calculate score for a single component based on its checks."""
    if not checks:
        return 100.0

    total_weight = 0.0
    weighted_score = 0.0

    for check in checks:
        status = check.get("status", "OK")
        category = check.get("category", "availability")
        weight = CHECK_WEIGHTS.get(category, 0.25)

        # Convert status to score
        if status == "OK":
            check_score = 100.0
        elif status == "WARNING":
            check_score = 70.0
        else:  # ERROR
            check_score = 30.0

        weighted_score += check_score * weight
        total_weight += weight

    if total_weight == 0:
        return 100.0

    return weighted_score / total_weight


def calculate_overall_score(components: dict[str, dict[str, Any]]) -> float:
    """Calculate overall health score from all components."""
    if not components:
        return 0.0

    total_weight = 0.0
    weighted_score = 0.0

    for name, component in components.items():
        score = component.get("score", 0)
        weight = COMPONENT_WEIGHTS.get(name, COMPONENT_WEIGHTS["default"])

        weighted_score += score * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return weighted_score / total_weight


def extract_issues(components: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract all issues from components, sorted by severity."""
    issues = []

    severity_order = {"ERROR": 0, "WARNING": 1, "OK": 2}

    for component_name, component in components.items():
        for check in component.get("checks", []):
            if check.get("status") in ("ERROR", "WARNING"):
                issues.append({
                    "component": component_name,
                    "check": check.get("name", "unknown"),
                    "severity": check.get("status"),
                    "message": check.get("message", ""),
                })

    # Sort by severity (ERROR first)
    issues.sort(key=lambda x: severity_order.get(x["severity"], 2))

    return issues


def extract_recommendations(components: dict[str, dict[str, Any]]) -> list[str]:
    """Extract all recommendations from components."""
    recommendations = []

    for component in components.values():
        recommendations.extend(component.get("recommendations", []))

    # Deduplicate while preserving order
    seen = set()
    unique_recommendations = []
    for rec in recommendations:
        if rec not in seen:
            seen.add(rec)
            unique_recommendations.append(rec)

    return unique_recommendations


def aggregate_reports(
    component_reports: list[dict[str, Any]],
    discovery_info: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Aggregate multiple component health reports into a unified report.

    Args:
        component_reports: List of health reports from individual agents
        discovery_info: Optional discovery metadata

    Returns:
        Unified health report
    """
    components = {}

    for report in component_reports:
        component_name = report.get("component", "Unknown")

        # Calculate component score if not provided
        if "score" not in report:
            report["score"] = calculate_component_score(report.get("checks", []))

        # Determine status if not provided
        if "status" not in report:
            report["status"] = determine_status(report["score"])

        components[component_name] = report

    # Calculate overall score
    overall_score = calculate_overall_score(components)
    overall_status = determine_status(overall_score)

    # Extract issues and recommendations
    issues = extract_issues(components)
    recommendations = extract_recommendations(components)

    # Build unified report
    report = {
        "cluster": discovery_info.get("cluster", "unknown") if discovery_info else "unknown",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "discovery": discovery_info or {},
        "detected_operators": discovery_info.get("detected_operators", []) if discovery_info else [],
        "components": components,
        "overall": {
            "status": overall_status,
            "score": round(overall_score, 1),
            "critical_issues": [i for i in issues if i["severity"] == "ERROR"],
            "warnings": [i for i in issues if i["severity"] == "WARNING"],
            "recommendations": recommendations,
        },
    }

    return report


def format_summary(report: dict[str, Any]) -> str:
    """Format report as human-readable summary."""
    lines = [
        f"# Cluster Health Report - {report['cluster']}",
        f"**Timestamp**: {report['timestamp']}",
        f"**Overall Status**: {report['overall']['status']} (Score: {report['overall']['score']})",
        "",
        "## Components",
    ]

    for name, component in report["components"].items():
        status_emoji = {"HEALTHY": "+", "DEGRADED": "~", "CRITICAL": "-"}.get(component["status"], "?")
        lines.append(f"  [{status_emoji}] {name}: {component['status']} ({component['score']})")

    if report["overall"]["critical_issues"]:
        lines.append("")
        lines.append("## Critical Issues")
        for issue in report["overall"]["critical_issues"]:
            lines.append(f"  - [{issue['component']}] {issue['check']}: {issue['message']}")

    if report["overall"]["recommendations"]:
        lines.append("")
        lines.append("## Recommendations")
        for rec in report["overall"]["recommendations"][:5]:  # Top 5
            lines.append(f"  - {rec}")

    return "\n".join(lines)


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Aggregate health reports")
    parser.add_argument("--reports-dir", help="Directory containing report JSON files")
    parser.add_argument("--discovery-json", help="Path to discovery JSON file")
    parser.add_argument(
        "--output",
        choices=["summary", "detailed", "json"],
        default="summary",
        help="Output format",
    )

    args = parser.parse_args()

    component_reports = []
    discovery_info = None

    # Load discovery info
    if args.discovery_json:
        with open(args.discovery_json) as f:
            discovery_info = json.load(f)

    # Load component reports from directory or stdin
    if args.reports_dir:
        import os
        for filename in os.listdir(args.reports_dir):
            if filename.endswith(".json"):
                with open(os.path.join(args.reports_dir, filename)) as f:
                    component_reports.append(json.load(f))
    elif not sys.stdin.isatty():
        # Try to read multiple JSON objects from stdin
        content = sys.stdin.read()
        try:
            # First try as JSON array
            component_reports = json.loads(content)
            if not isinstance(component_reports, list):
                component_reports = [component_reports]
        except json.JSONDecodeError:
            # Try line-by-line JSON
            for line in content.strip().split("\n"):
                if line:
                    component_reports.append(json.loads(line))

    # Aggregate reports
    report = aggregate_reports(component_reports, discovery_info)

    # Output based on format
    if args.output == "json":
        print(json.dumps(report, indent=2))
    elif args.output == "detailed":
        print(json.dumps(report, indent=2))
    else:  # summary
        print(format_summary(report))


if __name__ == "__main__":
    main()
