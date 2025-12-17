#!/usr/bin/env bash
# Docker-based Grafana development server
# Supports Grafana v12.x+ only

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
GRAFANA_VERSION="${GRAFANA_VERSION:-latest}"
GRAFANA_PORT="${GRAFANA_PORT:-3000}"
PLUGIN_DIR="${PLUGIN_DIR:-.}"

# Functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_debug() { echo -e "${BLUE}[DEBUG]${NC} $1"; }

usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] [COMMAND]

Docker-based Grafana development server for plugin development.

Commands:
  start       Start the development server (default)
  stop        Stop the development server
  restart     Restart the development server
  logs        Show Grafana logs
  status      Show server status

Options:
  -v, --version VERSION   Grafana version (default: latest)
  -p, --port PORT         Port to expose Grafana (default: 3000)
  -d, --dir DIR           Plugin directory (default: current directory)
  -h, --help              Show this help message

Environment Variables:
  GRAFANA_VERSION    Grafana Docker image version
  GRAFANA_PORT       Port to expose Grafana
  PLUGIN_DIR         Plugin directory path

Examples:
  $(basename "$0") start                    # Start with defaults
  $(basename "$0") -v 12.0.0 start          # Start with specific version
  $(basename "$0") -p 3001 start            # Start on port 3001
  $(basename "$0") logs                     # View Grafana logs
  $(basename "$0") stop                     # Stop the server
EOF
}

check_prerequisites() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop/"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running. Please start Docker Desktop."
        exit 1
    fi
}

check_plugin_dir() {
    if [ ! -f "$PLUGIN_DIR/plugin.json" ]; then
        log_error "plugin.json not found in $PLUGIN_DIR"
        log_error "Please run this script from a Grafana plugin directory"
        exit 1
    fi
}

get_plugin_id() {
    grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' "$PLUGIN_DIR/plugin.json" | head -1 | cut -d'"' -f4
}

start_server() {
    check_prerequisites
    check_plugin_dir

    PLUGIN_ID=$(get_plugin_id)
    log_info "Starting Grafana development server..."
    log_info "Plugin: $PLUGIN_ID"
    log_info "Grafana version: $GRAFANA_VERSION"
    log_info "Port: $GRAFANA_PORT"

    # Check if docker-compose.yaml exists
    if [ -f "$PLUGIN_DIR/docker-compose.yaml" ] || [ -f "$PLUGIN_DIR/docker-compose.yml" ]; then
        log_info "Using existing docker-compose.yaml"
        docker compose -f "$PLUGIN_DIR/docker-compose.yaml" up -d 2>/dev/null || \
        docker compose -f "$PLUGIN_DIR/docker-compose.yml" up -d
    else
        log_info "Starting standalone Grafana container..."
        docker run -d \
            --name "grafana-dev-$PLUGIN_ID" \
            -p "$GRAFANA_PORT:3000" \
            -v "$(cd "$PLUGIN_DIR" && pwd)/dist:/var/lib/grafana/plugins/$PLUGIN_ID" \
            -e "GF_DEFAULT_APP_MODE=development" \
            -e "GF_LOG_LEVEL=debug" \
            -e "GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS=$PLUGIN_ID" \
            "grafana/grafana:$GRAFANA_VERSION"
    fi

    echo ""
    log_info "Grafana is starting..."
    log_info "Access at: http://localhost:$GRAFANA_PORT"
    log_info "Login: admin / admin"
    echo ""
    log_info "Run 'npm run dev' to build and watch for changes"
}

stop_server() {
    check_plugin_dir

    PLUGIN_ID=$(get_plugin_id)
    log_info "Stopping Grafana development server..."

    if [ -f "$PLUGIN_DIR/docker-compose.yaml" ] || [ -f "$PLUGIN_DIR/docker-compose.yml" ]; then
        docker compose -f "$PLUGIN_DIR/docker-compose.yaml" down 2>/dev/null || \
        docker compose -f "$PLUGIN_DIR/docker-compose.yml" down 2>/dev/null || true
    fi

    docker stop "grafana-dev-$PLUGIN_ID" 2>/dev/null || true
    docker rm "grafana-dev-$PLUGIN_ID" 2>/dev/null || true

    log_info "Server stopped"
}

show_logs() {
    check_plugin_dir

    PLUGIN_ID=$(get_plugin_id)

    if [ -f "$PLUGIN_DIR/docker-compose.yaml" ] || [ -f "$PLUGIN_DIR/docker-compose.yml" ]; then
        docker compose -f "$PLUGIN_DIR/docker-compose.yaml" logs -f grafana 2>/dev/null || \
        docker compose -f "$PLUGIN_DIR/docker-compose.yml" logs -f grafana
    else
        docker logs -f "grafana-dev-$PLUGIN_ID"
    fi
}

show_status() {
    check_plugin_dir

    PLUGIN_ID=$(get_plugin_id)

    echo "Plugin: $PLUGIN_ID"
    echo "Directory: $PLUGIN_DIR"
    echo ""

    if docker ps --filter "name=grafana" --format "{{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -q .; then
        echo "Running containers:"
        docker ps --filter "name=grafana" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    else
        log_warn "No Grafana containers running"
    fi
}

# Parse arguments
COMMAND="start"

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--version)
            GRAFANA_VERSION="$2"
            shift 2
            ;;
        -p|--port)
            GRAFANA_PORT="$2"
            shift 2
            ;;
        -d|--dir)
            PLUGIN_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        start|stop|restart|logs|status)
            COMMAND="$1"
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Execute command
case $COMMAND in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        stop_server
        start_server
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
esac
