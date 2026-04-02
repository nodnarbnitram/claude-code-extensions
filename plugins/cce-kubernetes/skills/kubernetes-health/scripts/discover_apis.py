#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "kubernetes>=28.1.0",
# ]
# ///
"""
Kubernetes API Discovery Script

Discovers all API groups in a Kubernetes cluster and detects installed operators.
Returns a condensed JSON output suitable for agent consumption.

Usage:
    uv run discover_apis.py [--kubeconfig PATH] [--context NAME]
"""

import json
import sys
from typing import Any

try:
    from kubernetes import client, config
    from kubernetes.client.rest import ApiException
except ImportError:
    print(json.dumps({"error": "kubernetes package not installed", "hint": "Run: uv pip install kubernetes>=28.1.0"}))
    sys.exit(1)


# Known operator API groups and their names
KNOWN_OPERATORS = {
    "crossplane.io": "Crossplane",
    "apiextensions.crossplane.io": "Crossplane",
    "pkg.crossplane.io": "Crossplane",
    "argoproj.io": "ArgoCD",
    "cert-manager.io": "Cert-Manager",
    "acme.cert-manager.io": "Cert-Manager",
    "monitoring.coreos.com": "Prometheus",
    "flux.toolkit.fluxcd.io": "Flux",
    "source.toolkit.fluxcd.io": "Flux",
    "kustomize.toolkit.fluxcd.io": "Flux",
    "helm.toolkit.fluxcd.io": "Flux",
    "security.istio.io": "Istio",
    "networking.istio.io": "Istio",
    "gateway.networking.k8s.io": "Gateway API",
    "karpenter.sh": "Karpenter",
    "karpenter.k8s.aws": "Karpenter",
    "external-secrets.io": "External Secrets",
    "velero.io": "Velero",
}


def load_kube_config(kubeconfig: str | None = None, context: str | None = None) -> None:
    """Load Kubernetes configuration."""
    try:
        config.load_kube_config(config_file=kubeconfig, context=context)
    except config.ConfigException:
        try:
            config.load_incluster_config()
        except config.ConfigException as e:
            raise RuntimeError(f"Could not load Kubernetes config: {e}") from e


def discover_apis(kubeconfig: str | None = None, context: str | None = None) -> dict[str, Any]:
    """
    Discover all API groups and detect installed operators.

    Returns a condensed ClusterAPIMap structure.
    """
    load_kube_config(kubeconfig, context)

    api_client = client.ApiClient()

    result = {
        "cluster": "",
        "api_version": "",
        "core_resources": 0,
        "custom_resources": 0,
        "api_groups": [],
        "detected_operators": [],
    }

    # Get cluster info
    try:
        version_api = client.VersionApi(api_client)
        version_info = version_api.get_code()
        result["api_version"] = f"{version_info.major}.{version_info.minor}"
    except ApiException:
        result["api_version"] = "unknown"

    # Get current context name
    try:
        _, active_context = config.list_kube_config_contexts()
        result["cluster"] = active_context.get("context", {}).get("cluster", "unknown")
    except Exception:
        result["cluster"] = "unknown"

    # Discover core API (v1)
    try:
        core_api = client.CoreV1Api(api_client)
        api_resources = core_api.get_api_resources()
        result["core_resources"] = len(api_resources.resources)
    except ApiException as e:
        result["core_resources"] = 0
        result["error"] = f"Core API discovery failed: {e.reason}"

    # Discover all API groups
    try:
        apis_api = client.ApisApi(api_client)
        api_groups = apis_api.get_api_versions()

        seen_operators = set()

        for group in api_groups.groups:
            group_name = group.name
            result["api_groups"].append(group_name)

            # Check if this is a known operator
            if group_name in KNOWN_OPERATORS:
                operator_name = KNOWN_OPERATORS[group_name]
                if operator_name not in seen_operators:
                    seen_operators.add(operator_name)
                    result["detected_operators"].append({
                        "name": operator_name,
                        "api_group": group_name,
                        "status": "active",
                    })

        result["custom_resources"] = len(api_groups.groups)

    except ApiException as e:
        result["error"] = f"API group discovery failed: {e.reason}"

    return result


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Discover Kubernetes APIs")
    parser.add_argument("--kubeconfig", help="Path to kubeconfig file")
    parser.add_argument("--context", help="Kubernetes context to use")
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON output")

    args = parser.parse_args()

    try:
        result = discover_apis(kubeconfig=args.kubeconfig, context=args.context)

        if args.pretty:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(result))

    except RuntimeError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Unexpected error: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
