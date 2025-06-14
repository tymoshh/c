#! /usr/bin/env nix-shell
#! nix-shell -i bash -p bash openssh rsync

# Deployment script for remote server via SSH
# Usage: ./deploy.sh [ssh_key_path]

set -e  # Exit on any error

USER="mio"

# Configuration
REMOTE_HOST="${USER}@minionki.staszic.waw.pl"
SSH_KEY="${2:-~/.ssh/staszic}"
REMOTE_DIR="/home/k24_c/${USER}/.homepage/c"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log() {
    echo -e "$1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Validate prerequisites
validate_prerequisites() {
    # Test SSH connection
    log "Testing SSH connection to $REMOTE_HOST..."
    ssh -i "$SSH_KEY" -o ConnectTimeout=10 -o BatchMode=yes "$REMOTE_HOST" "echo 'SSH connection successful'" || error "Failed to connect to remote server"
}

# Deploy files
deploy_files() {
    log "Deploying files to remote server..."
    
    # Create remote directory if it doesn't exist
    ssh -i "$SSH_KEY" "$REMOTE_HOST" "mkdir -p $REMOTE_DIR"
    
    # Copy source files to remote homepage directory
    log "Copying source files to $REMOTE_HOST:$REMOTE_DIR"

    # Wipe the remote directory contents (including hidden files)
    ssh -i "$SSH_KEY" "$REMOTE_HOST" "find '$REMOTE_DIR' -mindepth 1 -delete 2>/dev/null || \
    find '$REMOTE_DIR' -mindepth 1 -exec rm -rf {} + 2>/dev/null"

    # Copy files recursively with compression and preservation
    scp -r -i "$SSH_KEY" -C "./src/." "$REMOTE_HOST:$REMOTE_DIR"
    
    # Copy pyproject.toml
    log "Copying pyproject.toml to remote server"
    scp -i "$SSH_KEY" "pyproject.toml" "$REMOTE_HOST:$REMOTE_DIR/"
    scp -i "$SSH_KEY" "uv.lock" "$REMOTE_HOST:$REMOTE_DIR/"
}

# Setup Python virtual environment
setup_venv() {
    log "Setting up Python virtual environment on remote server..."
    
    ssh -i "$SSH_KEY" "$REMOTE_HOST" << EOF
        cd '${REMOTE_DIR}'
        
        # Check if python3 is available
        if ! command -v uv &> /dev/null; then
            echo "Error: uv is not installed on the remote server"
            exit 1
        fi
        
        uv sync --locked --no-dev

        echo "${REMOTE_DIR}/utils" > "${REMOTE_DIR}/.venv/lib/python3.13/site-packages/dbcon.pth"
 
        echo "Virtual environment setup completed successfully"
EOF
}

# Set proper permissions for CGI
set_permissions() {
    log "Setting proper permissions for CGI files..."
    
    ssh -i "$SSH_KEY" "$REMOTE_HOST" << EOF
        cd '${REMOTE_DIR}'

        find ./ -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -print0 | xargs -0 chmod 644
        find ./ -type f \( -name "*.cgi" -o -name "*.py" \) -print0 | xargs -0 chmod 700

        # Make CGI files executable
        find . -name "*.cgi" -type f -exec chmod +x {} \;
        find . -name "*.py" -type f -exec chmod +x {} \;
        
        # Ensure proper directory permissions
        find . -type d -exec chmod 755 {} \;

        chmod +x run_cgi
EOF
    echo "Permissions set successfully"
}

# Main deployment function
main() {
    log "Starting deployment to $REMOTE_HOST"
    log "Using SSH key: $SSH_KEY"
    
    validate_prerequisites
    deploy_files
    setup_venv
    set_permissions
    
    log "Deployment completed successfully!"
    log "Your webpage is now deployed to $REMOTE_HOST:$REMOTE_DIR"
}

# Script usage
usage() {
    echo "Usage: $0 [ssh_key_path]"
    echo ""
    echo "Arguments:"
    echo "  ssh_key_path  Path to SSH private key (default: ~/.ssh/staszic)"
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 ~/.ssh/my_key"
    exit 1
}

# Handle help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    usage
fi

# Run main function
main "$@"