#!/usr/bin/env bash

# Reusable echo module with module name prefix
# Usage:
#   source /path/to/echo_module.sh
#   set_module_name "my-module"
#   echo "message"  # outputs: [my-module] message

MODULE_ECHO_NAME=""
DEBUG_DEVCODER="${DEBUG_DEVCODER:-false}"
if [ -n "${DEVCODER_LOG_DIR:-}" ]; then
    LOG_DIR="${DEVCODER_LOG_DIR}"
else
    CALLER_SOURCE="${BASH_SOURCE[1]:-}"
    if [ -n "$CALLER_SOURCE" ]; then
        LOG_DIR="$(cd "$(dirname "$CALLER_SOURCE")" && pwd)/logs"
    else
        LOG_DIR="$HOME/logs"
    fi
fi

if [ "${DEBUG_DEVCODER,,}" = "true" ]; then
    mkdir -p "$LOG_DIR"
fi

# Function to set the module name
set_module_name() {
    MODULE_ECHO_NAME="$1"
}

# Override the echo command to include module name prefix
echo() {
    local MESSAGE=""
    if [ -n "$MODULE_ECHO_NAME" ]; then
        MESSAGE="[$MODULE_ECHO_NAME] $*"
    else
        MESSAGE="$*"
    fi

    command echo "$MESSAGE"

    if [ "${DEBUG_DEVCODER,,}" = "true" ]; then
        mkdir -p "$LOG_DIR"
        local log_name="${MODULE_ECHO_NAME:-devcoder}.log"
        command echo "$MESSAGE" >> "$LOG_DIR/$log_name"
    fi
}

echo_legacy() {
    command echo "$*"
}