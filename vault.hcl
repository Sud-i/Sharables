storage "file" {
  path = "/vault/data"
}

listener "tcp" {
  address       = "0.0.0.0:8200"
  # Using .cer and .key files directly
  tls_cert_file = "/vault/certs/vault-server.cer"
  tls_key_file  = "/vault/certs/vault-server.key"
  tls_min_version = "tls12"
}

# Enable UI
ui = true

# API address
api_addr = "https://127.0.0.1:8200"

# Cluster address
cluster_addr = "https://127.0.0.1:8201"

# Disable mlock for Docker environment
disable_mlock = true

# Log level
log_level = "INFO"