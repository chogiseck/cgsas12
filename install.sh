#!/bin/bash
# Claude Code installer script
# Usage: curl -fsSL https://claude.ai/install.sh | bash
set -euo pipefail

BOLD='\033[1m'
DIM='\033[2m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

PACKAGE_NAME="@anthropic-ai/claude-code"
MIN_NODE_VERSION=18

info() {
    printf "${BOLD}${CYAN}%s${RESET}\n" "$*"
}

success() {
    printf "${GREEN}%s${RESET}\n" "$*"
}

warn() {
    printf "${YELLOW}Warning: %s${RESET}\n" "$*"
}

error() {
    printf "${RED}Error: %s${RESET}\n" "$*" >&2
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

version_gte() {
    # Returns 0 if $1 >= $2 (comparing major versions)
    [ "$1" -ge "$2" ] 2>/dev/null
}

get_node_major_version() {
    node --version 2>/dev/null | sed 's/^v//' | cut -d. -f1
}

detect_os() {
    case "$(uname -s)" in
        Linux*)  echo "linux" ;;
        Darwin*) echo "macos" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *)       echo "unknown" ;;
    esac
}

detect_arch() {
    case "$(uname -m)" in
        x86_64|amd64) echo "x64" ;;
        arm64|aarch64) echo "arm64" ;;
        *)             echo "unknown" ;;
    esac
}

install_via_npm() {
    info "Installing ${PACKAGE_NAME} via npm..."
    npm install -g "${PACKAGE_NAME}@latest"
}

check_node_installed() {
    if ! command_exists node; then
        return 1
    fi
    local major
    major="$(get_node_major_version)"
    if ! version_gte "$major" "$MIN_NODE_VERSION"; then
        return 1
    fi
    return 0
}

install_node_if_needed() {
    if check_node_installed; then
        local ver
        ver="$(node --version)"
        success "Node.js ${ver} detected."
        return 0
    fi

    if command_exists node; then
        local current
        current="$(node --version)"
        warn "Node.js ${current} found but version >= ${MIN_NODE_VERSION} is required."
    else
        warn "Node.js is not installed."
    fi

    info "Node.js >= ${MIN_NODE_VERSION} is required to run Claude Code."
    printf "\n"

    local os
    os="$(detect_os)"

    case "$os" in
        macos)
            if command_exists brew; then
                info "Installing Node.js via Homebrew..."
                brew install node
            else
                error "Please install Node.js >= ${MIN_NODE_VERSION} from https://nodejs.org"
                exit 1
            fi
            ;;
        linux)
            if command_exists apt-get; then
                info "Installing Node.js via NodeSource..."
                curl -fsSL "https://deb.nodesource.com/setup_${MIN_NODE_VERSION}.x" | bash -
                apt-get install -y nodejs
            elif command_exists dnf; then
                info "Installing Node.js via dnf..."
                dnf module install -y "nodejs:${MIN_NODE_VERSION}"
            elif command_exists yum; then
                info "Installing Node.js via NodeSource..."
                curl -fsSL "https://rpm.nodesource.com/setup_${MIN_NODE_VERSION}.x" | bash -
                yum install -y nodejs
            else
                error "Please install Node.js >= ${MIN_NODE_VERSION} from https://nodejs.org"
                exit 1
            fi
            ;;
        *)
            error "Please install Node.js >= ${MIN_NODE_VERSION} from https://nodejs.org"
            exit 1
            ;;
    esac

    if ! check_node_installed; then
        error "Node.js installation failed. Please install manually from https://nodejs.org"
        exit 1
    fi

    success "Node.js $(node --version) installed successfully."
}

verify_installation() {
    if command_exists claude; then
        local ver
        ver="$(claude --version 2>/dev/null || echo "unknown")"
        return 0
    fi
    return 1
}

main() {
    printf "\n"
    info "╔══════════════════════════════════════╗"
    info "║       Claude Code Installer          ║"
    info "╚══════════════════════════════════════╝"
    printf "\n"

    local os arch
    os="$(detect_os)"
    arch="$(detect_arch)"

    printf "${DIM}System: %s (%s)${RESET}\n" "$os" "$arch"
    printf "\n"

    # Step 1: Ensure Node.js is available
    install_node_if_needed
    printf "\n"

    # Step 2: Ensure npm is available
    if ! command_exists npm; then
        error "npm is not available. Please install npm and try again."
        exit 1
    fi

    # Step 3: Install Claude Code
    info "Installing Claude Code..."
    printf "\n"

    if install_via_npm; then
        printf "\n"
        if verify_installation; then
            success "============================================"
            success " Claude Code installed successfully!"
            success "============================================"
            printf "\n"
            printf " Run ${BOLD}claude${RESET} to get started.\n"
            printf "\n"
        else
            warn "Installation completed but 'claude' command not found in PATH."
            printf " You may need to restart your shell or add npm's global bin to PATH.\n"
            printf "\n"
            printf " Try running:\n"
            printf "   ${BOLD}export PATH=\"\$(npm prefix -g)/bin:\$PATH\"${RESET}\n"
            printf "\n"
        fi
    else
        printf "\n"
        error "Installation failed."
        printf "\n"
        printf " Troubleshooting:\n"
        printf "   - Check your internet connection\n"
        printf "   - Try: ${BOLD}npm install -g ${PACKAGE_NAME}@latest${RESET}\n"
        printf "   - If permission errors, see: https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally\n"
        printf "\n"
        exit 1
    fi
}

main "$@"
