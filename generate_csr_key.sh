#!/bin/bash

# Generate .cer and .key files for Vault (self-signed for development)
# In production, you'll replace these files with your CA-issued certificates

echo "=== Generating Self-Signed Certificate (.cer and .key) ==="

# Create certs directory
cd certs

# Configuration for the certificate
COUNTRY="IN"
STATE="Maharashtra"
CITY="Mumbai"
ORGANIZATION="Inspira Enterprise"
ORGANIZATIONAL_UNIT="Oneinspira"
COMMON_NAME="vault-server"  # This should match your container name or domain
EMAIL="admin@yourcompany.com"

# Subject line
SUBJECT="/C=${COUNTRY}/ST=${STATE}/L=${CITY}/O=${ORGANIZATION}/OU=${ORGANIZATIONAL_UNIT}/CN=${COMMON_NAME}/emailAddress=${EMAIL}"

echo "Creating certificate with:"
echo "Common Name: $COMMON_NAME"
echo "Organization: $ORGANIZATION"
echo ""

# Step 1: Generate private key (.key file)
echo "1. Generating private key (vault-server.key)..."
openssl genrsa -out vault-server.key 2048

# Step 2: Generate certificate signing request (CSR)
echo "2. Generating certificate signing request..."
openssl req -new -key vault-server.key -out vault-server.csr -subj "$SUBJECT"

# Step 3: Create config file for certificate extensions (SAN)
echo "3. Creating certificate extensions config..."
cat > vault-server.conf <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = $COUNTRY
ST = $STATE
L = $CITY
O = $ORGANIZATION
OU = $ORGANIZATIONAL_UNIT
CN = $COMMON_NAME
emailAddress = $EMAIL

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = vault-server
DNS.2 = localhost
DNS.3 = *.yourdomain.com
IP.1 = 127.0.0.1
IP.2 = 172.18.0.2
EOF

# Step 4: Generate self-signed certificate (.cer file)
echo "4. Generating self-signed certificate (vault-server.cer)..."
openssl x509 -req -in vault-server.csr -signkey vault-server.key -out vault-server.cer -days 365 -extensions v3_req -extfile vault-server.conf

# Step 5: Set proper permissions
echo "5. Setting file permissions..."
chmod 600 vault-server.key
chmod 644 vault-server.cer

# Step 6: Clean up temporary files
rm vault-server.csr vault-server.conf

echo ""
echo "✅ Certificate files generated successfully:"
echo "   📄 Certificate: $(pwd)/vault-server.cer"
echo "   🔐 Private Key: $(pwd)/vault-server.key"
echo ""

# Display certificate information
echo "=== Certificate Information ==="
openssl x509 -in vault-server.cer -text -noout | grep -E "Subject:|Issuer:|Not Before:|Not After:" | sed 's/^[[:space:]]*//'

echo ""
echo "=== Subject Alternative Names ==="
openssl x509 -in vault-server.cer -text -noout | grep -A 5 "Subject Alternative Name" | grep -E "DNS:|IP Address:" | sed 's/^[[:space:]]*//'

echo ""
echo "🔧 Next steps:"
echo "   1. Update your Vault configuration to use these files"
echo "   2. In production, replace these files with CA-issued certificates"
echo "   3. Keep the same file names and paths for easy replacement"

echo ""
echo "📝 For production deployment:"
echo "   - Replace vault-server.cer with your CA-issued .cer file"
echo "   - Replace vault-server.key with your CA-issued .key file"
echo "   - No configuration changes needed!"
