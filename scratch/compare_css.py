with open("dist/assets/index-CzgsKiV0.css", "r", encoding="utf-8") as f:
    css_main = f.read()

with open("v2-design-pro/dist/assets/index-CzgsKiV0.css", "r", encoding="utf-8") as f:
    css_v2 = f.read()

def get_leaflet_rules(content):
    rules = []
    import re
    # Simple regex to match selector and block {...}
    pattern = re.compile(r'([^{}]*leaflet[^{}]*)\{([^{}]*)\}')
    for m in pattern.finditer(content):
        rules.append((m.group(1).strip(), m.group(2).strip()))
    return rules

r_main = get_leaflet_rules(css_main)
r_v2 = get_leaflet_rules(css_v2)

print(f"Main Leaflet rules count: {len(r_main)}")
print(f"V2 Leaflet rules count: {len(r_v2)}")

print("=== V2 Leaflet Rules ===")
for sel, body in r_v2:
    print(f"{sel} {{ {body} }}")

print("=== Main Leaflet Rules ===")
for sel, body in r_main:
    print(f"{sel} {{ {body} }}")
