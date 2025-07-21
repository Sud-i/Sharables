ui = true
disable_mlock = true

storage "file" {
  path = "/vault/data"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = false
  tls_cert_file = "/vault/certs/vault.crt"
  tls_key_file = "/vault/certs/vault.key"
}

api_addr = "https://0.0.0.0:8200"
cluster_addr = "https://0.0.0.0:8201"

default_lease_ttl = "168h"
max_lease_ttl = "720h"

log_level = "Info"
log_file = "/vault/logs/vault.log"
log_rotate_duration = "24h"
log_rotate_max_files = 30