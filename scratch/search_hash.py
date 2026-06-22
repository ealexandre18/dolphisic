with open('c:/Users/Ewan Alexandre/Desktop/PROJET SDIS/dist/assets/index-DyRupmtp.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
for term in ['location.hash', 'hashchange', 'hash']:
    matches = [m.start() for m in re.finditer(re.escape(term), content, re.IGNORECASE)]
    print(f"Found {len(matches)} occurrences of '{term}'")
    for idx, pos in enumerate(matches[:5]):
        start = max(0, pos - 100)
        end = min(len(content), pos + 100)
        print(f"  Occurrence {idx+1}: {content[start:end].replace('\n', ' ')}")
