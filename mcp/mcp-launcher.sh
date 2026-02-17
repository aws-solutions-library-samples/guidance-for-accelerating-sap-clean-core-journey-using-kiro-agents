#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# CC_DIR: Clean Core root directory
# Auto-derive from script location if not set (script is in mcp/)
CC_DIR="${CC_DIR:-$(dirname "$SCRIPT_DIR")}"

# Validate CC_DIR exists
if [ ! -d "$CC_DIR" ]; then
  echo "ERROR: CC_DIR='$CC_DIR' does not exist" >&2
  exit 1
fi

docker run --rm -i --no-healthcheck --platform linux/amd64 \
  --mount type=bind,source="${CC_DIR}/secrets",target=/run/secrets,readonly \
  --env-file "${SCRIPT_DIR}/sap.env" \
  abap-accelerator-q:3.2.1-node22 2>&1 | while IFS= read -r line; do
  if [[ "$line" =~ ^\{.*\}$ ]]; then
    echo "$line"
  else
    echo "$line" >&2
  fi
done
