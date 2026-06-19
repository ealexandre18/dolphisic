with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js.bak", "r", encoding="utf-8") as f:
    content = f.read()

import re

# Let's search for "BIP" maps or lists
bip_matches = [m.start() for m in re.finditer(r'BIP', content)]
print(f"Found {len(bip_matches)} occurrences of 'BIP'")

# Let's search for the BIP list table:
# It's likely near the mapping of e.statut_activite or similar inside index-DyRupmtp.js
idx_statut = content.find("e.statut_activite===`inactif`?")
if idx_statut != -1:
    print(f"Found statut_activite mapping at index {idx_statut}")
    with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\scratch\bip_table_found.txt", "w", encoding="utf-8") as f:
        # Let's write the table container context (starting some chars before the status mapping)
        f.write(content[idx_statut-1000:idx_statut+1500])

# Active update key list
idx_active = content.find("e.date_maj_cle&&e.date_maj_cle.trim()!==``")
if idx_active == -1:
    # try single quote/backtick variations
    idx_active = content.find("date_maj_cle&&e.date_maj_cle.trim()!==\"\"")
if idx_active == -1:
    idx_active = content.find("date_maj_cle&&e.date_maj_cle.trim()!==''")
if idx_active == -1:
    # let's look for u.filter(e=>e.date_maj_cle
    idx_active = content.find("u.filter(e=>e.date_maj_cle")

print(f"Active key updates table map index: {idx_active}")
if idx_active != -1:
    with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\scratch\active_table_found.txt", "w", encoding="utf-8") as f:
        f.write(content[idx_active-1500:idx_active+2000])
