import sqlite3

def get_sites(path):
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT id, nom, latitude, longitude, type FROM sites ORDER BY id")
        return cur.fetchall()
    except Exception as e:
        return f"Error: {e}"

orig_sites = get_sites("scratch/carto_orig.db")
curr_sites = get_sites("carto_sdis04.db")
v2_sites = get_sites("v2-design-pro/carto_sdis04.db")

print("Orig sites count:", len(orig_sites) if isinstance(orig_sites, list) else orig_sites)
print("Curr sites count:", len(curr_sites) if isinstance(curr_sites, list) else curr_sites)
print("V2 sites count:", len(v2_sites) if isinstance(v2_sites, list) else v2_sites)

if isinstance(orig_sites, list) and isinstance(curr_sites, list):
    # check differences between orig and curr
    diff_orig_curr = []
    for o in orig_sites:
        if o not in curr_sites:
            diff_orig_curr.append(f"In Orig but not Curr: {o}")
    for c in curr_sites:
        if c not in orig_sites:
            diff_orig_curr.append(f"In Curr but not Orig: {c}")
    print("Diffs Orig <-> Curr:", len(diff_orig_curr))
    for d in diff_orig_curr[:10]:
        print(d)

if isinstance(v2_sites, list) and isinstance(curr_sites, list):
    # check differences between v2 and curr
    diff_v2_curr = []
    for v in v2_sites:
        if v not in curr_sites:
            diff_v2_curr.append(f"In V2 but not Curr: {v}")
    for c in curr_sites:
        if c not in v2_sites:
            diff_v2_curr.append(f"In Curr but not V2: {c}")
    print("Diffs V2 <-> Curr:", len(diff_v2_curr))
    for d in diff_v2_curr[:10]:
        print(d)
