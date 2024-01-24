import secrets

# Generate a random URL-safe string with 32 bytes (256 bits)
secret_key = secrets.token_urlsafe(32)

print("Your JWT secret key:", secret_key)
