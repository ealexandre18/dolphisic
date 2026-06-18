import sqlite3

def inspect_db(path):
    print(f"=== DB: {path} ===")
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    for t in tables:
        cur.execute(f"PRAGMA table_info({t})")
        cols = [f"{c[1]} ({c[2]})" for c in cur.fetchall()]
        print(f"Table: {t}")
        print(f"  Columns: {', '.join(cols)}")
        cur.execute(f"SELECT count(*) FROM {t}")
        print(f"  Rows: {cur.fetchone()[0]}")

inspect_db("sdis04.db")
inspect_db("v2-design-pro/sdis04.db")
