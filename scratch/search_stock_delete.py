import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\assets\index-DyRupmtp.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Search for /api/stock or /api/prets or delete queries related to stock
terms = [
    "stock",
    "prets",
    "/delete",
    "confirm",
]

matches = [m.start() for m in re.finditer("Supprimer", content)]
print("Found 'Supprimer' matches:", len(matches))
for m in matches:
    start = max(0, m - 100)
    end = min(len(content), m + 200)
    print(f"  [{m}]: ... {content[start:end]} ...\n")
