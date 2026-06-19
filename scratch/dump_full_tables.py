import sys

# Reconfigure stdout to handle UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js.bak", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find the Bips Pager Table headers and body map
# We search for: c==="BIP"?(0,P.jsxs)
idx_bip = content.find('c==="BIP"?')
if idx_bip != -1:
    print("=== BIP TABLE FULL SECTION ===")
    print(content[idx_bip:idx_bip+2500])
    print("\n" + "="*50 + "\n")

# Let's find the active key update table (contains date_maj_cle and date_cle_a_faire)
idx_active = content.find("date_maj_cle&&e.date_maj_cle.trim()!==``")
if idx_active != -1:
    print("=== ACTIVE KEY TABLE FULL SECTION ===")
    # Go back a bit to see the table / thead
    print(content[idx_active-1500:idx_active+2000])
    print("\n" + "="*50 + "\n")

# Let's find the pending key update table
idx_pending = content.find("u.filter(e=>!e.date_maj_cle||e.date_maj_cle.trim()===``)")
if idx_pending != -1:
    print("=== PENDING KEY TABLE FULL SECTION ===")
    print(content[idx_pending-500:idx_pending+2000])
    print("\n" + "="*50 + "\n")

# Let's find the search/all equipment table
idx_all = content.find("pe||`N/A`})})")
if idx_all != -1:
    print("=== ALL EQUIPMENT TABLE FULL SECTION ===")
    print(content[idx_all-1000:idx_all+2000])
    print("\n" + "="*50 + "\n")
