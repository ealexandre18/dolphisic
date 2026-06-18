import sqlite3

def dump_sites(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT id, nom, type FROM sites ORDER BY id")
    return cur.fetchall()

sites_main = dump_sites("carto_sdis04.db")
sites_v2 = dump_sites("v2-design-pro/carto_sdis04.db")

print("=== Main Sites ===")
for s in sites_main:
    print(s)

print("=== V2 Sites ===")
for s in sites_v2:
    print(s)
