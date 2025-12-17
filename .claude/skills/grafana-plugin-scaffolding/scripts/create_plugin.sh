#!/usr/bin/env bash
# Wrapper script for @grafana/create-plugin
# Supports Grafana v12.x+ only

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js is not installed. Please install Node.js v18+ from https://nodejs.org/"
        exit 1
    fi

    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        log_error "Node.js v18+ required. Current version: $(node -v)"
        exit 1
    fi
    log_info "Node.js $(node -v) - OK"

    # Check npm
    if ! command -v npm &> /dev/null; then
        log_error "npm is not installed."
        exit 1
    fi
    log_info "npm $(npm -v) - OK"

    # Check Docker (optional)
    if command -v docker &> /dev/null; then
        log_info "Docker $(docker --version | cut -d' ' -f3 | tr -d ',') - OK"
    else
        log_warn "Docker not found. Docker is recommended for local development."
    fi

    # Check Go (optional, for backend plugins)
    if command -v go &> /dev/null; then
        log_info "Go $(go version | cut -d' ' -f3 | tr -d 'go') - OK"
    else
        log_warn "Go not found. Required for backend plugins."
    fi
}

create_plugin() {
    log_info "Starting Grafana plugin scaffolding..."
    log_info "This will create a new plugin using @grafana/create-plugin"
    echo ""

    # Run the official scaffolder
    npx @grafana/create-plugin@latest "$@"
}

post_scaffold_instructions() {
    echo ""
    log_info "Plugin scaffolded successfully!"
    echo ""
    echo "Next steps:"
    echo "  1. cd <plugin-directory>"
    echo "  2. npm install"
    echo "  3. docker compose up -d   # Start Grafana with plugin"
    echo "  4. npm run dev            # Build and watch for changes"
    echo ""
    echo "Access Grafana at: http://localhost:3000"
    echo "Login: admin / admin"
    echo ""
    log_info "For more help, ask the grafana-plugin-expert agent"
}

# Main
main() {
    echo "==================================="
    echo "  Grafana Plugin Scaffolding"
    echo "  Supports: Grafana v12.x+"
    echo "==================================="
    echo ""

    check_prerequisites
    echo ""
    create_plugin "$@"
    post_scaffold_instructions
}

main "$@"
