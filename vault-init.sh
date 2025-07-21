#!/bin/bash

# Vault Production Initialization and Management Script

set -e

VAULT_ADDR="https://localhost:8200"
UNSEAL_KEYS_FILE="./vault-keys.json"
ROOT_TOKEN_FILE="./vault-root-token"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Wait for Vault to be ready
wait_for_vault() {
    log "Waiting for Vault to be ready..."
    local retries=30
    while [ $retries -gt 0 ]; do
        if vault status >/dev/null 2>&1; then
            break
        fi
        retries=$((retries - 1))
        sleep 2
    done
    
    if [ $retries -eq 0 ]; then
        error "Vault failed to start"
        exit 1
    fi
    log "Vault is ready"
}

# Initialize Vault
init_vault() {
    if [ -f "$UNSEAL_KEYS_FILE" ]; then
        warn "Vault appears to already be initialized"
        return
    fi
    
    log "Initializing Vault..."
    vault operator init \
        -key-shares=5 \
        -key-threshold=3 \
        -format=json > "$UNSEAL_KEYS_FILE"
    
    # Extract root token
    jq -r '.root_token' "$UNSEAL_KEYS_FILE" > "$ROOT_TOKEN_FILE"
    
    # Set secure permissions
    chmod 600 "$UNSEAL_KEYS_FILE" "$ROOT_TOKEN_FILE"
    
    log "Vault initialized successfully"
    warn "IMPORTANT: Store the unseal keys and root token securely!"
}

# Unseal Vault
unseal_vault() {
    if ! vault status | grep -q "Sealed.*true"; then
        log "Vault is already unsealed"
        return
    fi
    
    if [ ! -f "$UNSEAL_KEYS_FILE" ]; then
        error "Unseal keys file not found: $UNSEAL_KEYS_FILE"
        exit 1
    fi
    
    log "Unsealing Vault..."
    
    # Get first 3 unseal keys
    for i in 0 1 2; do
        key=$(jq -r ".unseal_keys_b64[$i]" "$UNSEAL_KEYS_FILE")
        vault operator unseal "$key"
    done
    
    log "Vault unsealed successfully"
}

# Enable audit logging
enable_audit() {
    if [ ! -f "$ROOT_TOKEN_FILE" ]; then
        error "Root token file not found: $ROOT_TOKEN_FILE"
        exit 1
    fi
    
    export VAULT_TOKEN=$(cat "$ROOT_TOKEN_FILE")
    
    log "Enabling audit logging..."
    vault audit enable file file_path=/vault/logs/audit.log
    
    log "Audit logging enabled"
}

# Setup basic auth methods and policies
setup_auth() {
    if [ ! -f "$ROOT_TOKEN_FILE" ]; then
        error "Root token file not found: $ROOT_TOKEN_FILE"
        exit 1
    fi
    
    export VAULT_TOKEN=$(cat "$ROOT_TOKEN_FILE")
    
    log "Setting up authentication methods..."
    
    # Enable userpass auth
    vault auth enable userpass
    
    # Create admin policy
    vault policy write admin - <<EOF
path "*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
EOF
    
    # Create read-only policy
    vault policy write readonly - <<EOF
path "secret/data/*" {
  capabilities = ["read", "list"]
}
EOF
    
    log "Authentication setup completed"
}

# Main execution
case "${1:-}" in
    "init")
        export VAULT_ADDR="$VAULT_ADDR"
        wait_for_vault
        init_vault
        ;;
    "unseal")
        export VAULT_ADDR="$VAULT_ADDR"
        unseal_vault
        ;;
    "setup")
        export VAULT_ADDR="$VAULT_ADDR"
        enable_audit
        setup_auth
        ;;
    "full")
        export VAULT_ADDR="$VAULT_ADDR"
        wait_for_vault
        init_vault
        unseal_vault
        enable_audit
        setup_auth
        ;;
    *)
        echo "Usage: $0 {init|unseal|setup|full}"
        echo "  init   - Initialize Vault"
        echo "  unseal - Unseal Vault"
        echo "  setup  - Setup audit and auth"
        echo "  full   - Run all steps"
        exit 1
        ;;
esac
