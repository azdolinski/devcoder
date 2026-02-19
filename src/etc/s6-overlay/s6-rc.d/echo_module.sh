#!/usr/bin/env bash

# Reusable logging module with module name prefix
# Usage:
#   source /path/to/echo_module.sh
#   set_module_name "my-module"
#   say "message"  # outputs: [my-module] message
#   echo "text" > file  # normal echo for file output

MODULE_ECHO_NAME=""
DEBUG_DEVCODER="${DEBUG_DEVCODER:-false}"
if [ -n "${DEVCODER_LOG_DIR:-}" ]; then
    LOG_DIR="${DEVCODER_LOG_DIR}"
else
    LOG_DIR="/var/log"
fi

if [ "${DEBUG_DEVCODER,,}" = "true" ]; then
    mkdir -p "$LOG_DIR"
fi

# Function to set the module name
set_module_name() {
    MODULE_ECHO_NAME="$1"
}

# Logging function with module name prefix - use for log messages
say() {
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