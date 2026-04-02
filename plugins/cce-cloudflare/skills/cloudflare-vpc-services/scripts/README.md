# Scripts

Utility scripts for working with Cloudflare VPC Services.

## Prerequisites

- wrangler installed: `npm install -g wrangler`
- logged in: `npx wrangler login`

## list-vpc-services.sh

Lists all VPC services in your Cloudflare account using `wrangler vpc service list`.

```bash
chmod +x list-vpc-services.sh
./list-vpc-services.sh
```

## tail-worker.sh

Tail logs from a deployed Worker to debug VPC connections.

```bash
./tail-worker.sh my-worker
./tail-worker.sh my-worker --errors-only
```

Useful for debugging `dns_error`, timeouts, and routing issues.

## set-api-token.sh

Set a secret for authenticating with private services.

```bash
./set-api-token.sh my-worker API_TOKEN
./set-api-token.sh my-worker PRIVATE_API_KEY
```

The secret will be available as `env.API_TOKEN` in your Worker code.
