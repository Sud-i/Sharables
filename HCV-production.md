# HashiCorp Vault Production Setup

## Quick Start

1. **Generate TLS certificates:**
   ```bash
   ./generate-certs.sh
   ```

2. **Start Vault:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Initialize and setup:**
   ```bash
   ./vault-init.sh full
   ```

## Security Considerations

- **TLS Certificates**: Use CA-signed certificates in production
- **Unseal Keys**: Store in separate secure locations (HSM, key management service)
- **Root Token**: Revoke after initial setup, use limited policies
- **Network**: Use private networks, VPN, or service mesh
- **Backups**: Implement automated encrypted backups
- **Monitoring**: Setup audit logging and metrics collection

## Files Created

- `vault-config.hcl` - Production Vault configuration
- `docker-compose.prod.yml` - Production Docker setup
- `vault-init.sh` - Initialization and management script
- `generate-certs.sh` - TLS certificate generation

## Important Notes

⚠️ **NEVER use in production without:**
- Proper TLS certificates from trusted CA
- Secure key management for unseal keys
- Network security (firewalls, VPN)
- Regular security audits
- Backup and disaster recovery plan
