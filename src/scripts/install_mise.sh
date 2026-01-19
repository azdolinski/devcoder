#!/bin/bash

# MISE-EN-PLACE - dev tools, env vars, task runner
# https://mise.jdx.dev/

# Install curl if not present
if ! command -v curl &> /dev/null; then
    sudo apt update && sudo apt install -y curl
fi

# Download the installer script:
sudo install -dm 755 /etc/apt/keyrings
curl -sSfL https://mise.jdx.dev/gpg-key.pub | gpg --dearmor | sudo tee /etc/apt/keyrings/mise-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/mise-archive-keyring.gpg arch=amd64] https://mise.jdx.dev/deb stable main" | sudo tee /etc/apt/sources.list.d/mise.list
sudo apt update
sudo apt install -y mise