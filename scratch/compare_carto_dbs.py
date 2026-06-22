import sqlite3
import os

root_carto = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\carto_sdis04.db"
redesign_carto = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\backend\carto_sdis04.db"

def inspect(path):
    print("Inspecting:", path)
    if not os.path.exists(path):
        print("  Does not exist!")
        return
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        print("  Tables:", tables)
        for t in tables:
            try:
                cur.execute(f"SELECT count(*) FROM [{t}]")
                print(f"    {t}: {cur.fetchone()[0]} rows")
            except Exception as e:
                print(f"    {t}: error querying count ({e})")
        conn.close()
    except Exception as e:
        print("  Error:", e)

inspect(root_carto)
inspect(redesign_carto)
