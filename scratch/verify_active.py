import hashlib

stored_hash = "020655a9e270fd2728cf65d5f331f065$49778fd5242cb17916291a5aca0db56903a13a03511760d8bd9c05a47ec1c414"
salt_hex, hash_hex = stored_hash.split("$")

candidates = ["sdis04", "T@mporaire04*", "admin", "cryptis"]

for cand in candidates:
    pwd_hash = hashlib.pbkdf2_hmac('sha256', cand.encode('utf-8'), bytes.fromhex(salt_hex), 100000)
    if pwd_hash.hex() == hash_hex:
        print(f"MATCH FOUND! Password is: {cand}")
        break
else:
    print("No match found.")
