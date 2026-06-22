import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Ewan Alexandre\Desktop\PROJET SDIS\dolphisic_redesign\public\assets\index-DyRupmtp.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

terms = [
    "/delete",
    "utilisateurs",
    "parc",
    "Ve = async",
    "Ve="
]

print(f"File length: {len(content)} chars")
for term in terms:
    matches = [m.start() for m in re.finditer(re.escape(term), content)]
    print(f"Term '{term}': found {len(matches)} matches")
    for idx in matches[:5]:
        start = max(0, idx - 80)
        end = min(len(content), idx + 200)
        print(f"  [{idx}]: ... {content[start:end]} ...\n")
