with open("dist/assets/index-DyRupmtp.js", "r", encoding="utf-8") as f:
    content = f.read()

import re
svgs = re.findall(r'<svg[^>]*>.*?</svg>', content, re.DOTALL)
print(f"Found {len(svgs)} SVG elements in JS file:")
for i, s in enumerate(svgs):
    print(f"SVG #{i}:")
    print(s[:500])
    print("-" * 50)
