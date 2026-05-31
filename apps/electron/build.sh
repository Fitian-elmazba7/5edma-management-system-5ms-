#!/bin/bash

# Electron build script
# Handles TypeScript compilation, Vite bundling, and electron-builder packaging

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
  echo -e "${GREEN}[Info]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[Warn]${NC} $1"
}

log_error() {
  echo -e "${RED}[Error]${NC} $1"
  exit 1
}

# Check prerequisites
log_info "Checking prerequisites..."

if ! command -v node &> /dev/null; then
  log_error "Node.js is not installed"
fi

if ! command -v npm &> /dev/null && ! command -v pnpm &> /dev/null; then
  log_error "npm or pnpm is not installed"
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
  log_error "Node.js 18+ is required (found v$(node -v))"
fi

log_info "Node.js $(node -v) detected"

# Clean old builds
log_info "Cleaning old builds..."
rm -rf dist build node_modules/.vite

# Install dependencies
log_info "Installing dependencies..."
npm install || pnpm install

# Compile TypeScript
log_info "Compiling TypeScript..."
npx tsc

# Bundle with Vite (if needed for preload/main)
# log_info "Bundling with Vite..."
# npx vite build

# Check if we should build installer
BUILD_INSTALLER=${1:-false}

if [ "$BUILD_INSTALLER" = "true" ] || [ "$BUILD_INSTALLER" = "--dist" ]; then
  log_info "Building Windows installer with electron-builder..."

  if [ ! -d "assets" ]; then
    log_warn "No assets directory found - installer will use defaults"
  fi

  npx electron-builder -w --publish never

  log_info "Installer created in dist/"
  ls -lh dist/*.exe 2>/dev/null || log_warn "No .exe file found"
else
  log_info "Skipping installer build (pass --dist to create)"
fi

log_info "Build complete!"
