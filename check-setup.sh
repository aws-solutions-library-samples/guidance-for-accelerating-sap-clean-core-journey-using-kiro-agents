#!/bin/bash
# =============================================================================
# SAP Clean Core Platform - Setup Checker
# =============================================================================
# Validates that the platform is correctly configured after installation.
# Run from any directory - paths are auto-derived from script location.
#
# Usage: ./check-setup.sh [OPTIONS]
#
# Options:
#   -h, --help            Show this help message
#   -q, --quiet           Exit code only (for CI/CD)
#   -j, --json            Machine-readable JSON output
#   -v, --verbose         Extra diagnostic detail
#   --test-connection     Test SAP connectivity via MCP server
#
# Exit codes:
#   0 - All checks passed
#   1 - Missing dependencies
#   2 - Missing files
#   3 - Permission errors
#   4 - Configuration errors
# =============================================================================

set -o pipefail
set -u

# -----------------------------------------------------------------------------
# Auto-derive CC_DIR from script location
# -----------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CC_DIR="${CC_DIR:-$SCRIPT_DIR}"

# -----------------------------------------------------------------------------
# Global variables
# -----------------------------------------------------------------------------
QUIET=false
JSON=false
VERBOSE=false
TEST_CONNECTION=false

# Counters
CHECKS_TOTAL=0
CHECKS_PASSED=0
CHECKS_FAILED=0
WARNINGS=0

# Exit code tracking (highest severity wins)
EXIT_CODE=0

# JSON data collectors
JSON_DEPS="{}"
JSON_WARNINGS="[]"
JSON_ERRORS="[]"

# Version info
DOCKER_VERSION=""
PYTHON_VERSION=""
KIRO_VERSION=""

# Check if python3 is available (for JSON operations)
HAS_PYTHON3=false
if python3 -c "import json" &> /dev/null; then
    HAS_PYTHON3=true
fi

# -----------------------------------------------------------------------------
# Output functions
# -----------------------------------------------------------------------------
log() {
    if [ "$QUIET" = false ] && [ "$JSON" = false ]; then
        echo "$@"
    fi
}

log_verbose() {
    if [ "$VERBOSE" = true ] && [ "$QUIET" = false ] && [ "$JSON" = false ]; then
        echo "  [verbose] $@"
    fi
}

log_check_pass() {
    ((CHECKS_TOTAL++))
    ((CHECKS_PASSED++))
    if [ "$QUIET" = false ] && [ "$JSON" = false ]; then
        echo "  ✓ $1"
    fi
}

log_check_fail() {
    local msg="$1"
    local code="$2"
    ((CHECKS_TOTAL++))
    ((CHECKS_FAILED++))
    if [ "$EXIT_CODE" -eq 0 ] || [ "$code" -lt "$EXIT_CODE" ]; then
        EXIT_CODE="$code"
    fi
    if [ "$QUIET" = false ] && [ "$JSON" = false ]; then
        echo "  ✗ $msg"
    fi
    if [ "$HAS_PYTHON3" = true ]; then
        JSON_ERRORS=$(MSG="$msg" python3 -c "import sys,json,os; d=json.load(sys.stdin); d.append(os.environ['MSG']); print(json.dumps(d))" <<< "$JSON_ERRORS")
    fi
}

log_check_warn() {
    ((CHECKS_TOTAL++))
    ((CHECKS_PASSED++))
    ((WARNINGS++))
    if [ "$QUIET" = false ] && [ "$JSON" = false ]; then
        echo "  ⚠ Warning: $1"
    fi
    if [ "$HAS_PYTHON3" = true ]; then
        JSON_WARNINGS=$(MSG="$1" python3 -c "import sys,json,os; d=json.load(sys.stdin); d.append(os.environ['MSG']); print(json.dumps(d))" <<< "$JSON_WARNINGS")
    fi
}

# -----------------------------------------------------------------------------
# Help function
# -----------------------------------------------------------------------------
show_help() {
    cat << 'EOF'
SAP Clean Core Platform - Setup Checker

Usage: ./check-setup.sh [OPTIONS]

Options:
  -h, --help            Show this help message
  -q, --quiet           Exit code only (for CI/CD)
  -j, --json            Machine-readable JSON output
  -v, --verbose         Extra diagnostic detail
  --test-connection     Test SAP connectivity via MCP server

Exit codes:
  0 - All checks passed
  1 - Missing dependencies
  2 - Missing files
  3 - Permission errors
  4 - Configuration errors

Examples:
  ./check-setup.sh                    # Full check with human-readable output
  ./check-setup.sh --quiet            # Silent, check exit code only
  ./check-setup.sh --json             # JSON output for automation
  ./check-setup.sh --test-connection  # Include SAP connectivity test
EOF
}

# -----------------------------------------------------------------------------
# Parse arguments
# -----------------------------------------------------------------------------
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -q|--quiet)
                QUIET=true
                shift
                ;;
            -j|--json)
                JSON=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            --test-connection)
                TEST_CONNECTION=true
                shift
                ;;
            *)
                echo "Unknown option: $1" >&2
                echo "Use --help for usage information" >&2
                exit 1
                ;;
        esac
    done
}

# -----------------------------------------------------------------------------
# Check: Dependencies
# -----------------------------------------------------------------------------
check_dependencies() {
    log ""
    log "[1/4] Checking dependencies..."
    log_verbose "CC_DIR=$CC_DIR"

    # Docker
    if command -v docker &> /dev/null; then
        # Docker binary exists, try to get version
        local docker_version_output
        local docker_version_exit
        docker_version_output=$(docker --version 2>&1)
        docker_version_exit=$?

        if [ $docker_version_exit -eq 0 ]; then
            DOCKER_VERSION=$(echo "$docker_version_output" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
            if [ -n "$DOCKER_VERSION" ]; then
                # Check if daemon is running
                local docker_info_output
                docker_info_output=$(docker info 2>&1)
                local docker_info_exit=$?

                if [ $docker_info_exit -eq 0 ]; then
                    log_check_pass "Docker: $DOCKER_VERSION (daemon running)"
                    if [ "$HAS_PYTHON3" = true ]; then
                        JSON_DEPS=$(VAL="$DOCKER_VERSION" python3 -c "import os,sys,json; d=json.load(sys.stdin); d['docker']=os.environ['VAL']; print(json.dumps(d))" <<< "$JSON_DEPS")
                    fi
                elif echo "$docker_info_output" | grep -qi "permission denied"; then
                    log_check_fail "Docker: $DOCKER_VERSION (permission denied - add user to docker group: sudo usermod -aG docker \$USER)" 3
                elif echo "$docker_info_output" | grep -qi "cannot connect\|connection refused\|Is the docker daemon running"; then
                    log_check_fail "Docker: $DOCKER_VERSION (daemon not running - start with: sudo systemctl start docker)" 1
                else
                    log_check_fail "Docker: $DOCKER_VERSION (cannot connect to daemon)" 1
                    log_verbose "Error: $docker_info_output"
                fi
            else
                log_check_fail "Docker: unable to parse version from: $docker_version_output" 1
            fi
        elif echo "$docker_version_output" | grep -qi "permission denied"; then
            log_check_fail "Docker: permission denied (add user to docker group: sudo usermod -aG docker \$USER, then log out and back in)" 3
        else
            log_check_fail "Docker: command failed: $docker_version_output" 1
        fi
    else
        log_check_fail "Docker: not installed (install from https://docs.docker.com/engine/install/)" 1
    fi

    # Python 3.8+
    if command -v python3 &> /dev/null; then
        local python_output
        python_output=$(python3 --version 2>&1)
        local python_exit=$?

        if [ $python_exit -eq 0 ]; then
            PYTHON_VERSION=$(echo "$python_output" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
            if [ -n "$PYTHON_VERSION" ]; then
                # Check version >= 3.8
                PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
                PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
                if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
                    log_check_pass "Python: $PYTHON_VERSION"
                    if [ "$HAS_PYTHON3" = true ]; then
                        JSON_DEPS=$(VAL="$PYTHON_VERSION" python3 -c "import os,sys,json; d=json.load(sys.stdin); d['python']=os.environ['VAL']; print(json.dumps(d))" <<< "$JSON_DEPS")
                    fi
                else
                    log_check_fail "Python: $PYTHON_VERSION (requires 3.8+, upgrade with your package manager)" 1
                fi
            else
                log_check_fail "Python: unable to parse version from: $python_output" 1
            fi
        else
            log_check_fail "Python: command failed: $python_output" 1
        fi
    else
        log_check_fail "Python3: not installed (install with your package manager, e.g., apt install python3)" 1
    fi

    # Kiro-CLI
    if command -v kiro-cli &> /dev/null; then
        local kiro_output
        kiro_output=$(kiro-cli --version 2>&1)
        local kiro_exit=$?

        if [ $kiro_exit -eq 0 ]; then
            KIRO_VERSION=$(echo "$kiro_output" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
            if [ -n "$KIRO_VERSION" ]; then
                log_check_pass "Kiro-CLI: $KIRO_VERSION"
                if [ "$HAS_PYTHON3" = true ]; then
                    JSON_DEPS=$(VAL="$KIRO_VERSION" python3 -c "import os,sys,json; d=json.load(sys.stdin); d['kiro']=os.environ['VAL']; print(json.dumps(d))" <<< "$JSON_DEPS")
                fi
            else
                # Version might not follow semver
                KIRO_VERSION=$(echo "$kiro_output" | head -1)
                log_check_pass "Kiro-CLI: $KIRO_VERSION"
                if [ "$HAS_PYTHON3" = true ]; then
                    JSON_DEPS=$(python3 -c "import sys,json; d=json.load(sys.stdin); d['kiro']='installed'; print(json.dumps(d))" <<< "$JSON_DEPS")
                fi
            fi
        else
            log_check_fail "Kiro-CLI: command failed: $kiro_output" 1
        fi
    else
        log_check_fail "Kiro-CLI: not installed (see installation instructions in README.md)" 1
    fi

    # Docker image: abap-accelerator-q:3.2.1-node22
    local docker_images_output
    docker_images_output=$(docker images --format "{{.Repository}}:{{.Tag}}" 2>&1)
    local docker_images_exit=$?

    if [ $docker_images_exit -eq 0 ]; then
        if echo "$docker_images_output" | grep -q "abap-accelerator-q:3.2.1-node22"; then
            log_check_pass "MCP Image: abap-accelerator-q:3.2.1-node22"
            if [ "$HAS_PYTHON3" = true ]; then
                JSON_DEPS=$(python3 -c "import sys,json; d=json.load(sys.stdin); d['mcp_image']='abap-accelerator-q:3.2.1-node22'; print(json.dumps(d))" <<< "$JSON_DEPS")
            fi
        else
            log_check_fail "MCP Image: abap-accelerator-q:3.2.1-node22 not found (pull or build the image)" 1
        fi
    elif echo "$docker_images_output" | grep -qi "permission denied"; then
        log_check_fail "MCP Image: cannot list images (permission denied - see Docker check above)" 3
    elif echo "$docker_images_output" | grep -qi "cannot connect\|connection refused"; then
        log_check_fail "MCP Image: cannot list images (Docker daemon not running)" 1
    else
        log_check_fail "MCP Image: cannot list images: $docker_images_output" 1
    fi
}

# -----------------------------------------------------------------------------
# Helper: Check file with better error messages
# -----------------------------------------------------------------------------
check_file_exists() {
    local filepath="$1"
    local display_path="$2"
    local hint="${3:-}"

    if [ -f "$filepath" ]; then
        log_check_pass "$display_path"
        return 0
    elif [ -e "$filepath" ]; then
        log_check_fail "$display_path: exists but is not a regular file" 2
        return 1
    else
        # Check if parent directory is accessible
        local parent_dir
        parent_dir=$(dirname "$filepath")
        if [ ! -d "$parent_dir" ]; then
            log_check_fail "$display_path: parent directory does not exist" 2
        elif [ ! -r "$parent_dir" ] || [ ! -x "$parent_dir" ]; then
            log_check_fail "$display_path: cannot access parent directory (permission denied)" 3
        elif [ -n "$hint" ]; then
            log_check_fail "$display_path: not found ($hint)" 2
        else
            log_check_fail "$display_path: not found" 2
        fi
        return 1
    fi
}

# -----------------------------------------------------------------------------
# Helper: Check directory with better error messages
# -----------------------------------------------------------------------------
check_dir_exists() {
    local dirpath="$1"
    local display_path="$2"

    if [ -d "$dirpath" ]; then
        if [ -r "$dirpath" ] && [ -x "$dirpath" ]; then
            log_check_pass "$display_path"
            return 0
        else
            log_check_fail "$display_path: exists but not accessible (permission denied)" 3
            return 1
        fi
    elif [ -e "$dirpath" ]; then
        log_check_fail "$display_path: exists but is not a directory" 2
        return 1
    else
        # Check if parent directory is accessible
        local parent_dir
        parent_dir=$(dirname "$dirpath")
        if [ ! -d "$parent_dir" ]; then
            log_check_fail "$display_path: parent directory does not exist" 2
        elif [ ! -r "$parent_dir" ] || [ ! -x "$parent_dir" ]; then
            log_check_fail "$display_path: cannot access parent directory (permission denied)" 3
        else
            log_check_fail "$display_path: directory not found" 2
        fi
        return 1
    fi
}

# -----------------------------------------------------------------------------
# Check: Files
# -----------------------------------------------------------------------------
check_files() {
    log ""
    log "[2/4] Checking files..."

    # Agent JSON configs (5 files)
    local agent_jsons=(
        "abap-accelerator.json"
        "sap-atc-checker.json"
        "sap-custom-code-documenter.json"
        "sap-unused-code-discovery.json"
        "business-function-mapper.json"
    )
    for json in "${agent_jsons[@]}"; do
        check_file_exists "$CC_DIR/.kiro/agents/$json" ".kiro/agents/$json"
    done

    # MCP launcher
    check_file_exists "$CC_DIR/mcp/mcp-launcher.sh" "mcp/mcp-launcher.sh"

    # sap.env
    check_file_exists "$CC_DIR/mcp/sap.env" "mcp/sap.env" "copy from sap.env.example"

    # secrets/ directory
    check_dir_exists "$CC_DIR/secrets" "secrets/"

    # sap_password
    check_file_exists "$CC_DIR/secrets/sap_password" "secrets/sap_password"

    # Agent instructions (5 files)
    local agent_dirs=(
        "abap-accelerator"
        "atc-checker"
        "documenter"
        "unused-code"
        "business-function-mapper"
    )
    for dir in "${agent_dirs[@]}"; do
        check_file_exists "$CC_DIR/agents/$dir/instructions.md" "agents/$dir/instructions.md"
    done

    # reports/ subdirectories
    local report_dirs=("atc" "docs" "unused" "executive")
    for dir in "${report_dirs[@]}"; do
        check_dir_exists "$CC_DIR/reports/$dir" "reports/$dir/"
    done

    # input/ directory
    check_dir_exists "$CC_DIR/input" "input/"
}

# -----------------------------------------------------------------------------
# Check: Permissions
# -----------------------------------------------------------------------------
check_permissions() {
    log ""
    log "[3/4] Checking permissions..."

    # mcp-launcher.sh executable
    if [ -x "$CC_DIR/mcp/mcp-launcher.sh" ]; then
        log_check_pass "mcp/mcp-launcher.sh: executable"
    else
        log_check_fail "mcp/mcp-launcher.sh: not executable (run: chmod +x mcp/mcp-launcher.sh)" 3
    fi

    # sap.env permissions (600 recommended)
    if [ -f "$CC_DIR/mcp/sap.env" ]; then
        if [ -r "$CC_DIR/mcp/sap.env" ]; then
            # Get permissions (cross-platform)
            local perms
            perms=$(ls -la "$CC_DIR/mcp/sap.env" | cut -c2-10)
            if [[ "$perms" == "rw-------" ]]; then
                log_check_pass "mcp/sap.env: 600"
            elif [[ "$perms" == "rw-r--r--" ]]; then
                log_check_warn "mcp/sap.env: 644 (recommend 600: chmod 600 mcp/sap.env)"
            else
                log_check_pass "mcp/sap.env: readable"
                log_verbose "Permissions: $perms"
            fi
        else
            log_check_fail "mcp/sap.env: not readable" 3
        fi
    fi

    # sap_password permissions (644 required for Docker MCP)
    # Note: 644 is needed because Kiro agents run MCP servers in Docker containers
    # that need to read the password file via bind mount
    if [ -f "$CC_DIR/secrets/sap_password" ]; then
        if [ -r "$CC_DIR/secrets/sap_password" ]; then
            local perms
            perms=$(ls -la "$CC_DIR/secrets/sap_password" | cut -c2-10)
            if [[ "$perms" == "rw-r--r--" ]]; then
                log_check_pass "secrets/sap_password: 644 (required for Docker MCP)"
            elif [[ "$perms" == "rw-------" ]]; then
                log_check_warn "secrets/sap_password: 600 (Docker MCP needs 644: chmod 644 secrets/sap_password)"
            else
                log_check_pass "secrets/sap_password: readable"
                log_verbose "Permissions: $perms"
            fi
        else
            log_check_fail "secrets/sap_password: not readable" 3
        fi
    fi

    # reports/ writable
    if [ -w "$CC_DIR/reports" ]; then
        log_check_pass "reports/: writable"
    else
        log_check_fail "reports/: not writable" 3
    fi
}

# -----------------------------------------------------------------------------
# Check: Configuration
# -----------------------------------------------------------------------------
check_configuration() {
    log ""
    log "[4/4] Validating configuration..."

    # sap.env required variables
    if [ -f "$CC_DIR/mcp/sap.env" ]; then
        local missing_vars=()
        local required_vars=("SAP_HOST" "SAP_USERNAME" "SAP_CLIENT")

        for var in "${required_vars[@]}"; do
            if ! grep -q "^${var}=" "$CC_DIR/mcp/sap.env" 2>/dev/null; then
                missing_vars+=("$var")
            else
                # Check if value is not empty or placeholder
                local val
                val=$(grep "^${var}=" "$CC_DIR/mcp/sap.env" | cut -d= -f2-)
                if [ -z "$val" ] || [ "$val" = "XXX" ] || [ "$val" = "hostname:port" ] || [ "$val" = "username" ]; then
                    missing_vars+=("$var (placeholder value)")
                fi
            fi
        done

        if [ ${#missing_vars[@]} -eq 0 ]; then
            log_check_pass "sap.env: SAP_HOST, SAP_USERNAME, SAP_CLIENT defined"
        else
            log_check_fail "sap.env: missing or placeholder values: ${missing_vars[*]}" 4
        fi
    fi

    # sap_password non-empty, no trailing newline
    if [ -f "$CC_DIR/secrets/sap_password" ]; then
        local pw_size
        pw_size=$(wc -c < "$CC_DIR/secrets/sap_password" | tr -d ' ')
        if [ "$pw_size" -eq 0 ]; then
            log_check_fail "sap_password: file is empty" 4
        else
            # Check for trailing newline
            local last_char
            last_char=$(tail -c 1 "$CC_DIR/secrets/sap_password" | od -An -tx1 | tr -d ' ')
            if [ "$last_char" = "0a" ]; then
                log_check_warn "sap_password: has trailing newline (use: echo -n 'password' > secrets/sap_password)"
            else
                log_check_pass "sap_password: non-empty, no trailing newline"
            fi
        fi
    fi

    # Agent JSONs valid
    local all_valid=true
    local agent_jsons=(
        "abap-accelerator.json"
        "sap-atc-checker.json"
        "sap-custom-code-documenter.json"
        "sap-unused-code-discovery.json"
        "business-function-mapper.json"
    )
    if [ "$HAS_PYTHON3" = true ]; then
        for json in "${agent_jsons[@]}"; do
            if [ -f "$CC_DIR/.kiro/agents/$json" ]; then
                if ! FPATH="$CC_DIR/.kiro/agents/$json" python3 -c "import os,json; json.load(open(os.environ['FPATH']))" 2>/dev/null; then
                    log_check_fail ".kiro/agents/$json: invalid JSON" 4
                    all_valid=false
                fi
            fi
        done
        if [ "$all_valid" = true ]; then
            log_check_pass "Agent configs: valid JSON"
        fi
    else
        log_check_warn "Agent configs: JSON validation skipped (python3 not available)"
    fi

    # Check if secrets are tracked by git (security warning)
    if [ -d "$CC_DIR/.git" ]; then
        local tracked_secrets=()
        if git -C "$CC_DIR" ls-files --error-unmatch mcp/sap.env &>/dev/null; then
            tracked_secrets+=("mcp/sap.env")
        fi
        if git -C "$CC_DIR" ls-files --error-unmatch secrets/sap_password &>/dev/null; then
            tracked_secrets+=("secrets/sap_password")
        fi
        if [ ${#tracked_secrets[@]} -gt 0 ]; then
            log_check_warn "Git tracking secrets: ${tracked_secrets[*]} (security risk - add to .gitignore)"
        fi
    fi

    # Check if input/ is empty (warning for unused-code-discovery)
    if [ -d "$CC_DIR/input" ]; then
        local input_count
        input_count=$(find "$CC_DIR/input" -type f 2>/dev/null | wc -l | tr -d ' ')
        if [ "$input_count" -eq 0 ]; then
            log_check_warn "input/ is empty (unused-code-discovery needs SUSG data)"
        fi
    fi
}

# -----------------------------------------------------------------------------
# Check: SAP Connection (optional)
# -----------------------------------------------------------------------------
check_connection() {
    if [ "$TEST_CONNECTION" = true ]; then
        log ""
        log "[Optional] Testing SAP connection..."

        if [ ! -f "$CC_DIR/mcp/mcp-launcher.sh" ]; then
            log_check_fail "SAP connection: mcp-launcher.sh not found" 2
            return
        fi

        if [ ! -x "$CC_DIR/mcp/mcp-launcher.sh" ]; then
            log_check_fail "SAP connection: mcp-launcher.sh not executable (run: chmod +x mcp/mcp-launcher.sh)" 3
            return
        fi

        # Send a simple MCP request to check connection
        local response
        local stderr_output
        stderr_output=$(mktemp)
        response=$(echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"aws_abap_cb_connection_status","arguments":{}},"id":1}' | \
            "$CC_DIR/mcp/mcp-launcher.sh" 2>"$stderr_output" | head -1)
        local mcp_exit=$?
        local stderr_content
        stderr_content=$(cat "$stderr_output" 2>/dev/null)
        rm -f "$stderr_output"

        if [ $mcp_exit -ne 0 ]; then
            if echo "$stderr_content" | grep -qi "permission denied"; then
                log_check_fail "SAP connection: permission denied running MCP launcher" 3
            elif echo "$stderr_content" | grep -qi "docker\|container"; then
                log_check_fail "SAP connection: Docker error - ensure Docker is running and accessible" 1
            else
                log_check_fail "SAP connection: MCP launcher failed (exit code $mcp_exit)" 4
            fi
            log_verbose "Stderr: $stderr_content"
            return
        fi

        if echo "$response" | grep -q '"result"'; then
            log_check_pass "SAP connection: successful"
        elif echo "$response" | grep -qi "authentication\|unauthorized\|401"; then
            log_check_fail "SAP connection: authentication failed (check SAP_USERNAME in sap.env and secrets/sap_password)" 4
        elif echo "$response" | grep -qi "connection refused\|connect\|timeout\|unreachable"; then
            log_check_fail "SAP connection: cannot reach SAP host (check SAP_HOST in sap.env)" 4
        elif echo "$response" | grep -qi "certificate\|ssl\|tls"; then
            log_check_fail "SAP connection: SSL/TLS error (check certificate configuration)" 4
        elif [ -z "$response" ]; then
            log_check_fail "SAP connection: no response from MCP server" 4
            log_verbose "Stderr: $stderr_content"
        else
            log_check_fail "SAP connection: unexpected response" 4
            log_verbose "Response: $response"
        fi
    fi
}

# -----------------------------------------------------------------------------
# Output JSON
# -----------------------------------------------------------------------------
output_json() {
    local status="pass"
    if [ "$EXIT_CODE" -ne 0 ]; then
        status="fail"
    fi

    STATUS="$status" \
    CHECKS_TOTAL="$CHECKS_TOTAL" \
    CHECKS_PASSED="$CHECKS_PASSED" \
    CHECKS_FAILED="$CHECKS_FAILED" \
    WARNINGS_COUNT="$WARNINGS" \
    EXIT_CODE_VAL="$EXIT_CODE" \
    JSON_DEPS="$JSON_DEPS" \
    JSON_WARNINGS="$JSON_WARNINGS" \
    JSON_ERRORS="$JSON_ERRORS" \
    python3 -c '
import json, os
result = {
    "status": os.environ["STATUS"],
    "checks": int(os.environ["CHECKS_TOTAL"]),
    "passed": int(os.environ["CHECKS_PASSED"]),
    "failed": int(os.environ["CHECKS_FAILED"]),
    "warnings": int(os.environ["WARNINGS_COUNT"]),
    "exit_code": int(os.environ["EXIT_CODE_VAL"]),
    "details": {
        "dependencies": json.loads(os.environ["JSON_DEPS"]),
        "warnings": json.loads(os.environ["JSON_WARNINGS"]),
        "errors": json.loads(os.environ["JSON_ERRORS"])
    }
}
print(json.dumps(result, indent=2))
'
}

# -----------------------------------------------------------------------------
# Output summary
# -----------------------------------------------------------------------------
output_summary() {
    log ""
    log "========================================"
    if [ "$EXIT_CODE" -eq 0 ]; then
        if [ "$WARNINGS" -gt 0 ]; then
            log "✓ All checks passed ($WARNINGS warning(s)). Platform ready."
        else
            log "✓ All $CHECKS_PASSED checks passed. Platform ready."
        fi
        log ""
        log "Run: kiro-cli agent list"
    else
        log "✗ $CHECKS_FAILED check(s) failed."
        log ""
        case $EXIT_CODE in
            1) log "Fix: Install missing dependencies" ;;
            2) log "Fix: Create missing files (see README.md)" ;;
            3) log "Fix: Correct file permissions" ;;
            4) log "Fix: Update configuration files" ;;
        esac
    fi
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
main() {
    parse_args "$@"

    # Python3 is required for --json mode
    if [ "$JSON" = true ] && ! python3 -c "import json" &> /dev/null; then
        echo '{"status":"fail","error":"python3 is required for --json mode but not installed"}' >&2
        exit 1
    fi

    # Header
    log "SAP Clean Core Platform - Setup Checker"
    log "========================================"

    # Run checks
    check_dependencies
    check_files
    check_permissions
    check_configuration
    check_connection

    # Output
    if [ "$JSON" = true ]; then
        output_json
    else
        output_summary
    fi

    exit "$EXIT_CODE"
}

main "$@"
