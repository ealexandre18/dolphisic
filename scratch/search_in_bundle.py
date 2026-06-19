import re
import sys

# Reconfigure stdout to handle UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dist\assets\index-DyRupmtp.js.bak"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for some patterns
patterns = [
    r"num_serie",
    r"affectation",
    r"date_maj_cle",
    r"statut_activite",
    r"date_cle_a_faire",
    r"date_prog",
    r"BIP"
]

print(f"File length: {len(content)} chars")
for pat in patterns:
    matches = [m.start() for m in re.finditer(pat, content)]
    print(f"Pattern '{pat}': found {len(matches)} matches")
    for idx in matches[:15]:
        start = max(0, idx - 100)
        end = min(len(content), idx + 200)
        print(f"  Context at {idx}: ... {content[start:end]} ...\n")
