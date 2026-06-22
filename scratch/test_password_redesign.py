import hashlib

stored_hash = "020655a9e270fd2728cf65d5f331f065$49778fd5242cb17916291a5aca0db56903a13a03511760d8bd9c05a47ec1c414"
salt_hex, hash_hex = stored_hash.split("$")

password = "sdis04"
pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt_hex), 100000)
if pwd_hash.hex() == hash_hex:
    print("MATCH! The redesign DB password is indeed sdis04.")
else:
    print(f"NO MATCH! Calculated: {pwd_hash.hex()} vs Stored: {hash_hex}")
