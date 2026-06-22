import hashlib
import sqlite3

def check_password(db_path, password):
    print("Checking database:", db_path)
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT identifiant, mot_de_passe FROM utilisateurs WHERE identifiant = 'admin'")
        row = cur.fetchone()
        if not row:
            print("  Admin user not found!")
            return
        username, stored_hash = row
        print(f"  Stored hash: {stored_hash}")
        salt_hex, hash_hex = stored_hash.split("$")
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt_hex), 100000)
        if pwd_hash.hex() == hash_hex:
            print("  SUCCESS! Password matches the stored hash.")
        else:
            print(f"  FAIL! Calculated hash {pwd_hash.hex()} does not match stored {hash_hex}.")
        conn.close()
    except Exception as e:
        print("  Error checking database:", e)

password = "T@mporaire04*"
check_password(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\sdis04.db", password)
check_password(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\backend\sdis04.db", password)
