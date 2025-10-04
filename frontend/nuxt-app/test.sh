#!/usr/bin/env bash
# Test script to verify frontend build

echo "🔍 Testing frontend configuration..."

echo "📁 Current directory:"
pwd

echo "📋 Environment variables:"
echo "NUXT_PUBLIC_API_BASE=${NUXT_PUBLIC_API_BASE:-'not set'}"

echo "📂 Checking .output directory:"
ls -la .output/ || echo "❌ .output directory not found"

echo "🎯 Checking server file:"
ls -la .output/server/index.mjs || echo "❌ Server file not found"

echo "🚀 Testing server start (dry run):"
echo "Would run: node .output/server/index.mjs"

echo "✅ Test complete"