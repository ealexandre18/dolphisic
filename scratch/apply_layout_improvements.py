# -*- coding: utf-8 -*-
import subprocess

js_path = r"dist/assets/index-DyRupmtp.js"
css_path = r"dist/assets/index-CzgsKiV0.css"

# 1. Update JS table
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

# Extract exact active targets (we already applied previous changes so we extract what's currently in JS)
exact_active_thead = get_exact_target("Active thead", "renouvellement", "(0,P.jsx)(`thead`", "]})})")
exact_active_tbody = get_exact_target("Active tbody", "renouvellement", "[...u.filter(e=>e.date_maj_cle", ",e.id))})")

# Define simplified replacements
rep_active_thead = "(0,P.jsx)(`thead`,{children:(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`th`,{children:`N\\u00b0 S\\u00e9rie`}),(0,P.jsx)(`th`,{children:`Mod\\u00e8le`}),(0,P.jsx)(`th`,{children:`Affectation`}),(0,P.jsx)(`th`,{children:`Date Limite`}),(0,P.jsx)(`th`,{children:`Statut Cl\\u00e9`}),(0,P.jsx)(`th`,{style:{textAlign:`center`},children:`Actions`})]})})"

rep_active_tbody = "[...u.filter(e=>e.date_maj_cle&&e.date_maj_cle.trim()!==``)].sort((e,t)=>{let n=Ye(e),r=Ye(t);return n===r?new Date(e.date_cle_a_faire||`9999-12-31`)-new Date(t.date_cle_a_faire||`9999-12-31`):n-r}).map(e=>(0,P.jsxs)(`tr`,{style:{backgroundColor:I(e)},children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.modele||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{children:e.date_cle_a_faire||`Non d\\u00e9finie`}),(0,P.jsx)(`td`,{children:Xe(e.date_cle_a_faire)}),(0,P.jsxs)(`td`,{style:F.actionsCell,children:[(0,P.jsx)(`button`,{title:`Mettre \\u00e0 jour la cl\\u00e9`,onClick:()=>He(e),style:{...F.actionBtn,color:`#f4a261`,background:`rgba(244, 162, 97, 0.1)`},children:(0,P.jsx)(me,{size:14})}),(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...F.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),(0,P.jsx)(`button`,{title:e.notification_active?`Alerte active (${e.email_notif}) - Cliquer pour modifier`:`Activer une alerte par email`,onClick:()=>Se(e),style:{...F.actionBtn,color:e.notification_active?`#4ade80`:`var(--text-muted)`,background:e.notification_active?`rgba(74, 222, 128, 0.15)`:`rgba(255,255,255,0.05)`},children:e.notification_active?(0,P.jsx)(re,{size:14}):(0,P.jsx)(ne,{size:14})}),(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})])})]},e.id))})"

# Clean up brackets
rep_active_tbody = rep_active_tbody.replace("])})", "]})")

# Replace in JS
new_js_content = content.replace(exact_active_thead, rep_active_thead)
new_js_content = new_js_content.replace(exact_active_tbody, rep_active_tbody)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(new_js_content)

print("JS Active table simplified!")

# Verify JS Syntax
res = subprocess.run(["node", "--check", js_path], capture_output=True, text=True)
if res.returncode == 0:
    print("JS Syntax check PASSED!")
else:
    print("JS Syntax check FAILED:")
    print(res.stderr[:500])
    exit(1)

# 2. Update CSS padding
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# Replace padding:14px 18px with padding:8px 12px
new_css_content = css_content.replace("padding:14px 18px", "padding:8px 12px")

with open(css_path, "w", encoding="utf-8") as f:
    f.write(new_css_content)

print("CSS cell padding reduced successfully!")
