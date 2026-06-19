# -*- coding: utf-8 -*-
import subprocess

js_path = r"dist/assets/index-DyRupmtp.js"

# Reset file to HEAD
subprocess.run(["git", "checkout", js_path])

with open(js_path, "r", encoding="utf-8") as f:
    content = f.read()

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

target = get_exact_target("BIP tbody", "Bips Pager", "u.map(e=>(0,P.jsxs)(`tr`", ",e.id))})")

# Corrected replacement: changed `])})` to `]})`
replacement = "u.map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.modele||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{children:e.statut_activite===`inactif`?(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(230, 57, 70, 0.15)`,color:`#e63946`},children:`Inactif`}):(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(74, 222, 128, 0.15)`,color:`#4ade80`},children:`Actif`})}),(0,P.jsxs)(`td`,{style:F.actionsCell,children:[(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...F.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})]})]},e.id))})"

new_content = content.replace(target, replacement)
with open(js_path, "w", encoding="utf-8") as f:
    f.write(new_content)

res = subprocess.run(["node", "--check", js_path], capture_output=True, text=True)
if res.returncode == 0:
    print("SUCCESS: Syntax check passed!")
else:
    print("FAILED:")
    print(res.stderr[:500])
