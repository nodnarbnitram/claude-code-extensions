#!/bin/bash
# Set API token secret for authenticating with private services
#
# Usage: ./set-api-token.sh <worker-name> <secret-name>

set -e

WORKER_NAME="$1"
SECRET_NAME="${2:-API_TOKEN}"

if [ -z "$WORKER_NAME" ]; then
  echo "Usage: ./set-api-token.sh <worker-name> [secret-name]"
  echo ""
  echo "Examples:"
  echo "  ./set-api-token.sh my-worker"
  echo "  ./set-api-token.sh my-worker PRIVATE_API_KEY"
  exit 1
fi

echo "Setting secret '$SECRET_NAME' for worker: $WORKER_NAME"
echo "Enter the secret value (will be hidden):"

npx wrangler secret put "$SECRET_NAME" --name "$WORKER_NAME"

echo ""
echo "Secret set. Access it in your Worker as: env.$SECRET_NAME"
