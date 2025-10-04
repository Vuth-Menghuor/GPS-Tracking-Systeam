#!/usr/bin/env bash
# Render build script for Nuxt.js

set -o errexit  # exit on error

# Install dependencies
npm ci

# Build the application for production
npm run build