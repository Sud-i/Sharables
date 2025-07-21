#!/bin/bash

# Generate TLS certificates for Vault production

set -e

CERT_DIR="./certs"
DOMAIN="hrms.inspiraenterprise.local"
DAYS=365

# Create certs directory
mkdir -p "$CERT_DIR"

echo "Generating TLS certificates for Vault..."

# Generate private key
openssl genrsa -out "$CERT_DIR/vault.key" 2048

# Generate certificate signing request
openssl req -new -key "$CERT_DIR/vault.key" -out "$CERT_DIR/vault.csr" -subj "/C=IN/ST=Maharashtra/L=Mumbai/O=Inspira Enterprise/OU=IT/CN=$DOMAIN"

# Generate self-signed certificate (for development/testing)
openssl x509 -req -in "$CERT_DIR/vault.csr" -signkey "$CERT_DIR/vault.key" -out "$CERT_DIR/vault.crt" -days $DAYS -extensions v3_req -extfile <(
cat <<EOF
[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = $DOMAIN
DNS.2 = localhost
IP.1 = 127.0.0.1
EOF
)

# Set appropriate permissions
chmod 600 "$CERT_DIR/vault.key"
chmod 644 "$CERT_DIR/vault.crt"

# Clean up CSR
rm "$CERT_DIR/vault.csr"

echo "Certificates generated in $CERT_DIR/"
echo "IMPORTANT: For production, use certificates from a trusted CA!"
echo "Update DOMAIN variable in this script and vault-config.hcl with your actual domain"
