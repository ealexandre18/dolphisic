# -*- coding: utf-8 -*-

js_path = r"dist/assets/index-DyRupmtp.js"
content = open(js_path, encoding='utf-8').read()

def get_exact_target(label, start_lbl, look_for, end_marker, offset=0):
    idx_lbl = content.find(start_lbl)
    if idx_lbl == -1:
        raise ValueError(f"Could not find label: {start_lbl}")
    idx_start = content.find(look_for, idx_lbl)
    if idx_start == -1:
        raise ValueError(f"Could not find look_for: {look_for} after label")
    idx_end = content.find(end_marker, idx_start)
    if idx_end == -1:
        raise ValueError(f"Could not find end_marker: {end_marker}")
    idx_end += len(end_marker) + offset
    return content[idx_start:idx_end]

targets = {
    "bip_thead": get_exact_target("BIP thead", "Bips Pager", "(0,P.jsx)(`thead`", "]})})"),
    "bip_tbody": get_exact_target("BIP tbody", "Bips Pager", "u.map(e=>(0,P.jsxs)(`tr`", ",e.id))})"),
    "active_thead": get_exact_target("Active thead", "renouvellement", "(0,P.jsx)(`thead`", "]})})"),
    "active_tbody": get_exact_target("Active tbody", "renouvellement", "[...u.filter(e=>e.date_maj_cle", ",e.id))})"),
    "pending_thead": get_exact_target("Pending thead", "En attente de premier cryptage", "(0,P.jsx)(`thead`", "]})})"),
    "pending_tbody": get_exact_target("Pending tbody", "(0,P.jsx)(`tbody`,{children:u.filter(e=>!e.date_maj_cle", "u.filter(e=>!e.date_maj_cle", ",e.id))})")
}

for name, target in targets.items():
    count = content.count(target)
    print(f"Target '{name}': count = {count}")
