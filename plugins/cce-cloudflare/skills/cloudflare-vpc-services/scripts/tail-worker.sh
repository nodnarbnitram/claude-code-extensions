#!/bin/bash
# Tail logs from a deployed Worker to debug VPC service connections
#
# Usage: ./tail-worker.sh <worker-name> [--errors-only]

set -e

WORKER_NAME="$1"
FILTER=""

if [ -z "$WORKER_NAME" ]; then
  echo "Usage: ./tail-worker.sh <worker-name> [--errors-only]"
  echo ""
  echo "Examples:"
  echo "  ./tail-worker.sh my-worker"
  echo "  ./tail-worker.sh my-worker --errors-only"
  exit 1
fi

if [ "$2" = "--errors-only" ]; then
  FILTER="--status error"
fi

echo "Tailing logs for worker: $WORKER_NAME"
echo "Press Ctrl+C to stop"
echo ""

npx wrangler tail "$WORKER_NAME" $FILTER --format pretty
