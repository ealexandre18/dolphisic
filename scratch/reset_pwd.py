import sqlite3
import hashlib
import os

salt_hex = "012eea623422611c767fb8cdb96761ba"
new_password = "sdis04"

# Compute PBKDF2 hash
pwd_hash = hashlib.pbkdf2_hmac('sha256', new_password.encode('utf-8'), bytes.fromhex(salt_hex), 100000)
new_stored_hash = f"{salt_hex}${pwd_hash.hex()}"

dbs = [
    "c:/Users/Ewan Alexandre/Desktop/PROJET SDIS/v3-design-pro/sdis04.db",
    "c:/Users/Ewan Alexandre/Desktop/PROJET SDIS/sdis04.db"
]

for db_path in dbs:
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("UPDATE utilisateurs SET mot_de_passe = ? WHERE identifiant = ?", (new_stored_hash, "admin"))
        conn.commit()
        print(f"Updated password in {db_path} to '{new_password}'")
        conn.close()
    else:
        print(f"Path does not exist: {db_path}")
