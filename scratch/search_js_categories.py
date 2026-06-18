with open("dist/assets/index-DyRupmtp.js", "r", encoding="utf-8") as f:
    content = f.read()

import re
for term in ["Bips", "Portatifs", "Mobiles", "Tous"]:
    matches = [m.start() for m in re.finditer(term, content)]
    print(f"Term '{term}': {len(matches)} matches")
    for idx in matches:
        print("  ", content[max(0, idx-60):min(len(content), idx+60)])
