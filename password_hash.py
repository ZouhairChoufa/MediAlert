import base64
import hashlib

def scrypt_hash(password, salt_separator=b'\x07', rounds=8, mem_cost=14):
    """Hash password using SCRYPT with Firebase config"""
    n = 2 ** mem_cost
    r = rounds
    p = 1
    
    # Combine password with salt separator
    password_bytes = password.encode('utf-8') + salt_separator
    
    # Generate hash
    hash_bytes = hashlib.scrypt(
        password_bytes,
        salt=b'',
        n=n,
        r=r,
        p=p,
        dklen=64
    )
    
    return base64.b64encode(hash_bytes).decode('utf-8')

def verify_password(password, stored_hash):
    """Verify password against stored hash"""
    computed_hash = scrypt_hash(password)
    return computed_hash == stored_hash
