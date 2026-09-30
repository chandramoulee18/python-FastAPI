from passlib.context import CryptContext

import hashlib
import bcrypt

def _prehash(password:str) ->bytes:
    # 1. Encode the String password to Byte
    # 2. Pre-hash with SHA-256 to fit within bcrypt's 72-byte limit
    # using .digest() returns raw bytes (32 bytes long)
    
    return hashlib.sha256(password.encode('utf-8')).digest()

def hash_password(password:str) -> str:
    prehashed = _prehash(password)
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(prehashed,salt).decode('utf-8')

    return hashedPassword

def verify_password(plain_password:str,stored_hash:str) -> bool:
    prehashed = _prehash(plain_password)
    return bcrypt.checkpw(prehashed,stored_hash.encode('utf-8'))

# pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# def hashPassword(password:str)->bytes:
#     #1. Encode the String password to Byte
#     password_bytes = password.encode('utf-8')

#     # 2. Pre-hash with SHA-256 to fit within bcrypt's 72-byte limit
#     # using .digest() returns raw bytes (32 bytes long)
#     sha256_hash = hashlib.sha256(password_bytes).digest()

#      # 3. Hash with bcrypt
#     salt = bcrypt.gensalt()
#     hashedPassword = bcrypt.hashpw(sha256_hash,salt).decode('utf-8')

#     return hashedPassword

# def verifyPassword(plain_password:str,hashed_password:str)->bool:

#     print(f"DEBUG - Hashed password value: {hashed_password}")
#     print(f"DEBUG - Data type: {type(hashed_password)}")

#     test_password = "my_secret_password"

#     # 1. Simulate Registration (Hash generation)
#     hashed_out = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#     print(f"Generated Hash: {hashed_out}")

#     # 2. Simulate Login (Verification)
#     is_match = bcrypt.checkpw(test_password.encode('utf-8'), hashed_out.encode('utf-8'))
#     print(f"Does it match in-memory?: {is_match}")

#     if not hashed_password:
#         return False
#     #if hashPassword(plain_password) != hashed_password:
#         #return False #

#     plain_password_hashed = hashPassword(plain_password)

#     #return True
#     #return pwd_context.verify(plain_password,hashed_password)
#     # return bcrypt.checkpw(
#     #     plain_password.encode('utf-8'),
#     #     hashed_password.encode('utf-8')
#     # )
#     print(f"DEBUG - Hashed password value: {hashed_password}")
#     print(f"DEBUG - Hashed password value for Login Password: {plain_password_hashed}")
    
#     if plain_password_hashed == hashed_password:
#         return True

#     return False

