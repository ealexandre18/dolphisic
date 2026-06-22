with open('c:/Users/Ewan Alexandre/Desktop/PROJET SDIS/dist/assets/index-DyRupmtp.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(re.escape('stock'), content, re.IGNORECASE)]

print(f"Found {len(matches)} occurrences of 'stock'")

for idx, pos in enumerate(matches[:15]):
    start = max(0, pos - 100)
    end = min(len(content), pos + 100)
    snippet = content[start:end]
    print(f"\n--- Occurrence {idx+1} (position {pos}) ---")
    print(snippet.replace('\n', ' '))
