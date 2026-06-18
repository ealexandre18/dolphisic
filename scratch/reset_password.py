import sqlite3
import hashlib
import os

password = "T@mporaire04*"

# Génère un nouveau salt et hash avec PBKDF2-SHA256 (même algo que server.py)
salt = os.urandom(16)
pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
stored = salt.hex() + "$" + pwd_hash.hex()

# Met à jour la base
conn = sqlite3.connect('sdis04.db')
cur = conn.cursor()
cur.execute("UPDATE utilisateurs SET mot_de_passe = ? WHERE identifiant = 'admin'", (stored,))
conn.commit()

# Vérifie
cur.execute("SELECT identifiant, mot_de_passe FROM utilisateurs WHERE identifiant = 'admin'")
row = cur.fetchone()
conn.close()

print(f"Mot de passe mis à jour pour : {row[0]}")
print(f"Hash stocké : {row[1][:40]}...")

# Vérifie que le hash est correct
salt_hex, hash_hex = row[1].split("$")
verify = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt_hex), 100000)
print(f"Vérification : {'OK ✓' if verify.hex() == hash_hex else 'ECHEC ✗'}")
