import re
import os

js_dir = 'c:/Users/Ewan Alexandre/Desktop/PROJET SDIS/dist/assets/'
js_files = [f for f in os.listdir(js_dir) if f.endswith('.js')]

print("Found JS files:", js_files)

for jf in js_files:
    path = os.path.join(js_dir, jf)
    print(f"Reading {path}...")
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Search for occurrences of 'stock' or similar strings
    matches = re.findall(r"['\"][^'\"]*?stock[^'\"]*?['\"]", content, re.IGNORECASE)
    print(f"Found {len(matches)} matches in {jf}:")
    for m in set(matches[:30]):
        # Print safely in cp1252
        print(m.encode('ascii', errors='replace').decode('ascii'))
