with open(r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js.bak", "r", encoding="utf-8") as f:
    content = f.read()

# statutory activity match 1 (Bips list mapping)
idx1 = 237802
print("=== BIP LIST MAP CONTEXT ===")
print(content[idx1-200:idx1+1000])
print("\n")

# statutory activity match 2 (All equipment search list mapping)
idx2 = 264431
print("=== ALL EQUIPMENT MAP CONTEXT ===")
print(content[idx2-200:idx2+1000])
print("\n")

# Let's also look for key updates pending and active lists.
# In the search results for date_cle_a_faire, we saw:
# - Context at 240381 (which maps date_cle_a_faire and Xe(e.date_cle_a_faire))
# Let's check Context at 240381
idx3 = 240381
print("=== KEY TABLE 1 MAP CONTEXT ===")
print(content[idx3-250:idx3+1000])
print("\n")

# And let's look for u.filter(e=>!e.date_maj_cle||e.date_maj_cle.trim()===``) or similar.
# Let's search the file for "!e.date_maj_cle"
import re
idx4 = content.find("!e.date_maj_cle")
if idx4 != -1:
    print("=== KEY TABLE 2 MAP CONTEXT ===")
    print(content[idx4-200:idx4+1000])
