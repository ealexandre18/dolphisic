import sqlite3

def compare_dbs(db1, db2):
    print(f"Comparing {db1} and {db2}...")
    conn1 = sqlite3.connect(db1)
    conn2 = sqlite3.connect(db2)
    cur1 = conn1.cursor()
    cur2 = conn2.cursor()
    
    cur1.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables1 = set(r[0] for r in cur1.fetchall())
    cur2.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables2 = set(r[0] for r in cur2.fetchall())
    
    if tables1 != tables2:
        print("Different tables!")
        print("Only in 1:", tables1 - tables2)
        print("Only in 2:", tables2 - tables1)
    
    common_tables = tables1.intersection(tables2)
    for table in common_tables:
        if table == 'sqlite_sequence':
            continue
        cur1.execute(f"SELECT * FROM {table}")
        rows1 = set(tuple(r) for r in cur1.fetchall())
        cur2.execute(f"SELECT * FROM {table}")
        rows2 = set(tuple(r) for r in cur2.fetchall())
        
        if rows1 != rows2:
            print(f"Table '{table}' has differences:")
            only_1 = rows1 - rows2
            only_2 = rows2 - rows1
            print(f"  Only in {db1} ({len(only_1)} rows):")
            for r in list(only_1)[:5]:
                print("   ", r)
            print(f"  Only in {db2} ({len(only_2)} rows):")
            for r in list(only_2)[:5]:
                print("   ", r)

compare_dbs("carto_sdis04.db", "v2-design-pro/carto_sdis04.db")
compare_dbs("sdis04.db", "v2-design-pro/sdis04.db")
