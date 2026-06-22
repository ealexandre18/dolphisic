import re

js_file = 'c:/Users/Ewan Alexandre/Desktop/PROJET SDIS/dist/assets/index-DyRupmtp.js'

with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's search for UI labels or button labels in React components.
# In React, children are often written as: children:"Label" or "Label" in JSX transpiled code (e.g. (0,P.jsx)("button", { ... children: "Label" }))
matches = re.findall(r'children:\s*["\']([^"\']{2,40})["\']', content)
print("--- Button/Label candidates in compiled JSX (children) ---")
for m in sorted(list(set(matches))):
    if any(keyword in m.lower() for keyword in ['stock', 'recherche', 'stat', 'mat', 'carto', 'table', 'param']):
        print(f"candidate: {m}")

# Let's search for strings in general that match any of our keywords
print("\n--- Any string literal candidates ---")
all_strings = re.findall(r'["\']([^"\']{2,50})["\']', content)
for s in sorted(list(set(all_strings))):
    if any(keyword in s.lower() for keyword in ['stock', 'recherche', 'stat', 'mat', 'carto', 'table', 'param']):
        print(f"string literal: {s}")
