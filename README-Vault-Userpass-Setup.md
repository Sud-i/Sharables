# Vault Userpass Authentication Setup Guide

This guide provides a comprehensive walkthrough for setting up username/password authentication in HashiCorp Vault.

## Prerequisites

- HashiCorp Vault server running and accessible
- Vault initialized and unsealed
- Root token or sufficient privileges to enable auth methods
- Vault CLI available

## Step-by-Step Setup

### 1. Authenticate with Root Token

First, authenticate to Vault using your root token:

```bash
# Set the root token as environment variable
export VAULT_TOKEN=your_root_token_here

# Or login directly
vault login your_root_token_here
```

### 2. Enable Userpass Auth Method

Enable the userpass authentication method:

```bash
# Enable userpass auth method
vault auth enable userpass

# Verify it's enabled
vault auth list
```

Expected output:
```
Path         Type        Accessor                  Description
----         ----        --------                  -----------
token/       token       auth_token_xxxxx          token based credentials
userpass/    userpass    auth_userpass_xxxxx       n/a
```

### 3. Create Users

Create users with passwords and assign policies:

```bash
# Create a user with basic access
vault write auth/userpass/users/admin \
    password=admin123 \
    policies=default

# Create additional users with specific policies
vault write auth/userpass/users/developer \
    password=dev456 \
    policies=dev-policy

# Create read-only user
vault write auth/userpass/users/readonly \
    password=readonly789 \
    policies=read-only-policy
```

### 4. Create Custom Policies (Optional)

Create custom policies for different user roles:

```bash
# Create a developer policy
vault policy write dev-policy - <<EOF
# Allow full access to secret/dev path
path "secret/dev/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Allow read access to secret/shared
path "secret/shared/*" {
  capabilities = ["read", "list"]
}
EOF

# Create a read-only policy
vault policy write read-only-policy - <<EOF
# Allow read access to all secrets
path "secret/*" {
  capabilities = ["read", "list"]
}
EOF
```

### 5. Test User Authentication

Test the newly created users:

```bash
# Login with username/password
vault login -method=userpass username=admin password=admin123

# Or use environment variables
export VAULT_AUTH_METHOD=userpass
export VAULT_USERNAME=admin
export VAULT_PASSWORD=admin123
vault login -method=$VAULT_AUTH_METHOD username=$VAULT_USERNAME password=$VAULT_PASSWORD
```

### 6. User Management Commands

#### List Users
```bash
vault list auth/userpass/users
```

#### View User Details
```bash
vault read auth/userpass/users/admin
```

#### Update User Password
```bash
vault write auth/userpass/users/admin password=new_password123
```

#### Update User Policies
```bash
vault write auth/userpass/users/admin policies=default,dev-policy
```

#### Delete User
```bash
vault delete auth/userpass/users/username
```

## Docker Environment Setup

If running Vault in Docker (as in this project):

### 1. Enable Userpass in Container
```bash
# Using environment variable
docker exec vault-prod sh -c 'export VAULT_TOKEN=your_root_token && vault auth enable -tls-skip-verify userpass'

# Create user in container
docker exec vault-prod sh -c 'export VAULT_TOKEN=your_root_token && vault write -tls-skip-verify auth/userpass/users/admin password=admin123 policies=default'
```

### 2. Test Login in Container
```bash
docker exec vault-prod vault login -tls-skip-verify -method=userpass username=admin password=admin123
```

## Configuration Best Practices

### 1. Password Policies
Configure password requirements:

```bash
# Create password policy
vault write auth/userpass/users/admin \
    password=secure_password \
    password_policy=strong-passwords \
    policies=default
```

### 2. Token TTL Configuration
Set token time-to-live values:

```bash
vault write auth/userpass/users/admin \
    password=admin123 \
    policies=default \
    token_ttl=1h \
    token_max_ttl=24h
```

### 3. MFA Integration (Enterprise)
For Vault Enterprise, enable multi-factor authentication:

```bash
# Enable TOTP MFA
vault write auth/userpass/mfa_config type=totp issuer="MyCompany Vault"

# Require MFA for user
vault write auth/userpass/users/admin \
    password=admin123 \
    policies=default \
    mfa_methods=totp
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure you're authenticated with sufficient privileges
2. **Auth Method Not Found**: Verify userpass is enabled with `vault auth list`
3. **Invalid Password**: Check password meets any configured password policies
4. **Token Expired**: Re-authenticate or extend token TTL

### Debug Commands
```bash
# Check current authentication
vault token lookup

# Verify user exists
vault read auth/userpass/users/username

# Check auth method configuration
vault read auth/userpass/config

# View audit logs (if enabled)
vault read sys/audit
```

## Security Considerations

1. **Use Strong Passwords**: Implement password policies for complexity requirements
2. **Regular Rotation**: Rotate passwords regularly
3. **Principle of Least Privilege**: Assign minimal necessary policies to users
4. **Audit Logging**: Enable audit logging to track authentication events
5. **TLS Encryption**: Always use TLS in production environments
6. **MFA**: Enable multi-factor authentication for sensitive accounts

## Integration Examples

### Bash Script Authentication
```bash
#!/bin/bash
VAULT_ADDR="https://vault.example.com:8200"
USERNAME="admin"
PASSWORD="admin123"

# Login and get token
VAULT_TOKEN=$(vault login -method=userpass \
    -field=token \
    username="$USERNAME" \
    password="$PASSWORD")

export VAULT_TOKEN
echo "Authenticated successfully"
```

### Python Integration
```python
import hvac

# Initialize client
client = hvac.Client(url='https://vault.example.com:8200')

# Authenticate
client.auth.userpass.login(
    username='admin',
    password='admin123'
)

# Use client for operations
secret = client.secrets.kv.v2.read_secret_version(path='myapp/config')
```

## References

- [HashiCorp Vault Userpass Auth Method Documentation](https://www.vaultproject.io/docs/auth/userpass)
- [Vault Policies Documentation](https://www.vaultproject.io/docs/concepts/policies)
- [Vault API Documentation](https://www.vaultproject.io/api-docs)