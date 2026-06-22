import sqlite3

db_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\backend\sdis04.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT identifiant, mot_de_passe, role FROM utilisateurs")
rows = cur.fetchall()
print("Users in DB:")
for r in rows:
    print(f"Username: {r[0]}, Hash: {r[1]}, Role: {r[2]}")
conn.close()
