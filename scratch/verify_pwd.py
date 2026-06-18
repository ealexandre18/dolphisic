import hashlib

stored_hash = "012eea623422611c767fb8cdb96761ba$a13708c9db1d5fc56144fa4908f010d3932411ad1ed2098e4d737f989e8cf9ea"
salt_hex, hash_hex = stored_hash.split("$")

candidates = ["admin", "sdis04", "sdis", "password", "123456", "cryptis"]

for cand in candidates:
    pwd_hash = hashlib.pbkdf2_hmac('sha256', cand.encode('utf-8'), bytes.fromhex(salt_hex), 100000)
    if pwd_hash.hex() == hash_hex:
        print(f"MATCH FOUND! Password is: {cand}")
        break
else:
    print("No match found in basic list.")
