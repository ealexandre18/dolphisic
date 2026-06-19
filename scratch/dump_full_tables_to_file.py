with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js.bak", "r", encoding="utf-8") as f:
    content = f.read()

import re

output = []

# 1. Bips Table
idx_bip = content.find('c==="BIP"?')
if idx_bip != -1:
    output.append("=== BIP TABLE FULL SECTION ===")
    output.append(content[idx_bip:idx_bip+2500])
    output.append("\n" + "="*50 + "\n")
else:
    output.append("=== BIP TABLE NOT FOUND ===\n")

# 2. Active Key Table
idx_active = content.find("date_maj_cle&&e.date_maj_cle.trim()!==``")
if idx_active != -1:
    output.append("=== ACTIVE KEY TABLE FULL SECTION ===")
    output.append(content[idx_active-1500:idx_active+2000])
    output.append("\n" + "="*50 + "\n")
else:
    output.append("=== ACTIVE KEY TABLE NOT FOUND ===\n")

# 3. Pending Key Table
idx_pending = content.find("u.filter(e=>!e.date_maj_cle||e.date_maj_cle.trim()===``)")
if idx_pending != -1:
    output.append("=== PENDING KEY TABLE FULL SECTION ===")
    output.append(content[idx_pending-500:idx_pending+2000])
    output.append("\n" + "="*50 + "\n")
else:
    output.append("=== PENDING KEY TABLE NOT FOUND ===\n")

# 4. All Equipment Table
idx_all = content.find("pe||`N/A`})})")
if idx_all != -1:
    output.append("=== ALL EQUIPMENT TABLE FULL SECTION ===")
    output.append(content[idx_all-1000:idx_all+2000])
    output.append("\n" + "="*50 + "\n")
else:
    output.append("=== ALL EQUIPMENT TABLE NOT FOUND ===\n")

with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\scratch\tables_raw.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Dumped tables raw context successfully to scratch/tables_raw.txt")
