#!/bin/bash
# List VPC services for your Cloudflare account
#
# Prerequisites:
#   - wrangler installed: npm install -g wrangler
#   - logged in: npx wrangler login

set -e

echo "Listing VPC services..."
echo ""

npx wrangler vpc service list
