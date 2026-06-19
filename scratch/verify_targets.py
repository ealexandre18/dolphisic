# -*- coding: utf-8 -*-
import os

js_path = r"dist/assets/index-DyRupmtp.js"
if not os.path.exists(js_path):
    print("JS file does not exist!")
    exit(1)

content = open(js_path, encoding='utf-8').read()
print("Total length:", len(content))

def locate(label, start_lbl, look_for, end_marker, offset=0):
    idx_lbl = content.find(start_lbl)
    if idx_lbl == -1:
        print(f"Error: could not find label: {repr(start_lbl)}")
        return
    idx_start = content.find(look_for, idx_lbl)
    if idx_start == -1:
        print(f"Error: could not find look_for: {repr(look_for)} after label")
        return
    idx_end = content.find(end_marker, idx_start)
    if idx_end == -1:
        print(f"Error: could not find end_marker: {repr(end_marker)}")
        return
    idx_end += len(end_marker) + offset
    sub = content[idx_start:idx_end]
    print(f"FOUND {label} ({idx_start} to {idx_end}):")
    print(sub[:150] + " ... " + sub[-150:])
    print("-" * 60)

locate("BIP thead", "Bips Pager", "(0,P.jsx)(`thead`", "]})})")
locate("BIP tbody", "Bips Pager", "u.map(e=>(0,P.jsxs)(`tr`", ",e.id))})")

locate("Active thead", "renouvellement", "(0,P.jsx)(`thead`", "]})})")
locate("Active tbody", "renouvellement", "[...u.filter(e=>e.date_maj_cle", ",e.id))})")

locate("Pending thead", "En attente de premier cryptage", "(0,P.jsx)(`thead`", "]})})")
locate("Pending tbody", "(0,P.jsx)(`tbody`,{children:u.filter(e=>!e.date_maj_cle", "u.filter(e=>!e.date_maj_cle", ",e.id))})")
