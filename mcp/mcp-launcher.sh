#!/bin/bash
# MCP HTTP Server Launcher
# Reads SAP config from mcp/sap.env and secrets/sap_password
#
# Usage: ./mcp/mcp-launcher.sh
# Starts FastMCP server on http://localhost:8001/mcp

set -euo pipefail

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Load SAP config and export all variables
SAP_ENV="$PROJECT_ROOT/mcp/sap.env"
if [[ -f "$SAP_ENV" ]]; then
    set -a
    # shellcheck source=/dev/null
    source "$SAP_ENV"
    set +a
else
    echo "Error: mcp/sap.env not found" >&2
    exit 1
fi

# Read password from secrets (avoids exposing in process list)
SAP_PASSWORD_FILE="$PROJECT_ROOT/secrets/sap_password"
if [[ -f "$SAP_PASSWORD_FILE" ]]; then
    SAP_PASSWORD=$(<"$SAP_PASSWORD_FILE")
    SAP_PASSWORD="${SAP_PASSWORD%$'\n'}"  # Trim trailing newline
    export SAP_PASSWORD
else
    echo "Error: secrets/sap_password not found" >&2
    exit 1
fi

# Set server defaults
export SERVER_HOST="${SERVER_HOST:-localhost}"
export SERVER_PORT="${SERVER_PORT:-8001}"
export FASTMCP_STATELESS_HTTP=true
export SSL_VERIFY="${SAP_SECURE:-false}"
export LOG_LEVEL="${LOG_LEVEL:-ERROR}"

# Validate port is numeric
if ! [[ "$SERVER_PORT" =~ ^[0-9]+$ ]]; then
    echo "Error: SERVER_PORT must be numeric, got: $SERVER_PORT" >&2
    exit 1
fi

# Path to server
SERVER_DIR="$PROJECT_ROOT/aws-abap-accelerator-http"
VENV_PYTHON="$SERVER_DIR/venv/bin/python"

if [[ ! -d "$SERVER_DIR/src/aws_abap_accelerator" ]]; then
    echo "Error: Server directory not found at $SERVER_DIR/src/aws_abap_accelerator" >&2
    exit 1
fi

if [[ ! -x "$VENV_PYTHON" ]]; then
    echo "Error: Python venv not found at $SERVER_DIR/venv" >&2
    echo "Run: cd $SERVER_DIR && python3.11 -m venv venv && venv/bin/pip install -r requirements.txt" >&2
    exit 1
fi

# Start server
cd "$SERVER_DIR/src/aws_abap_accelerator"
exec "$VENV_PYTHON" -c "
from server.fastmcp_server import ABAPAcceleratorServer
from config.settings import get_settings

server = ABAPAcceleratorServer(get_settings())
server.run('streamable-http')
"
