import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\assets\index-DyRupmtp.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

pos = content.find("Le=async()=>{")
if pos != -1:
    # search forwards for any occurrences of "Le()" or similar
    matches = [m.start() for m in re.finditer(r"\bLe\b", content)]
    print("Found 'Le' occurrences:", len(matches))
    for m in matches:
        start = max(0, m - 50)
        end = min(len(content), m + 100)
        print(f"  [{m}]: ... {content[start:end]} ...\n")
else:
    print("Not found")
