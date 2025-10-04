#!/usr/bin/env bash
# Render build script for Nuxt.js

set -o errexit  # exit on error

# Install dependencies
npm ci

# Build the application for production
npm run build

# Make sure the server file is executable
chmod +x .output/server/index.mjs