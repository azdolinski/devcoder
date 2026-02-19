#!/bin/bash

# Download the installer script:
curl -fsSL https://get.pulumi.com | sh
# curl -fsSL https://get.pulumi.com | sh -s -- --version <version>
# curl -fsSL https://get.pulumi.com | sh -s -- --version dev

# Add Pulumi to PATH
export PATH="$HOME/.pulumi/bin:$PATH"
echo 'export PATH="$HOME/.pulumi/bin:$PATH"' >> $HOME/.bashrc

# Verify the installation:
pulumi version
