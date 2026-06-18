import sqlite3
conn = sqlite3.connect('sdis04.db')
cur = conn.cursor()
cur.execute("PRAGMA table_info(utilisateurs)")
cols = cur.fetchall()
print("Colonnes de la table utilisateurs:")
for c in cols:
    print(f"  {c[1]} ({c[2]})")
print()
cur.execute("SELECT * FROM utilisateurs")
for r in cur.fetchall():
    print(r)
conn.close()
