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

# Extract exact targets
exact_bip_thead = get_exact_target("BIP thead", "Bips Pager", "(0,P.jsx)(`thead`", "]})})")
exact_bip_tbody = get_exact_target("BIP tbody", "Bips Pager", "u.map(e=>(0,P.jsxs)(`tr`", ",e.id))})")

exact_active_thead = get_exact_target("Active thead", "renouvellement", "(0,P.jsx)(`thead`", "]})})")
exact_active_tbody = get_exact_target("Active tbody", "renouvellement", "[...u.filter(e=>e.date_maj_cle", ",e.id))})")

exact_pending_thead = get_exact_target("Pending thead", "En attente de premier cryptage", "(0,P.jsx)(`thead`", "]})})")
exact_pending_tbody = get_exact_target("Pending tbody", "(0,P.jsx)(`tbody`,{children:u.filter(e=>!e.date_maj_cle", "u.filter(e=>!e.date_maj_cle", ",e.id))})")

# Corrected Replacements (with correct brackets `]})`)
# 1. BIP thead
rep_bip_thead = "(0,P.jsx)(`thead`,{children:(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`th`,{children:`N\\u00b0 S\\u00e9rie`}),(0,P.jsx)(`th`,{children:`Mod\\u00e8le`}),(0,P.jsx)(`th`,{children:`Affectation`}),(0,P.jsx)(`th`,{children:`Statut`}),(0,P.jsx)(`th`,{style:{textAlign:`center`},children:`Actions`})]})})"

# 2. BIP tbody
rep_bip_tbody = "u.map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.modele||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{children:e.statut_activite===`inactif`?(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(230, 57, 70, 0.15)`,color:`#e63946`},children:`Inactif`}):(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(74, 222, 128, 0.15)`,color:`#4ade80`},children:`Actif`})}),(0,P.jsxs)(`td`,{style:F.actionsCell,children:[(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...F.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})])})]},e.id))})"

# 3. Active thead
rep_active_thead = "(0,P.jsx)(`thead`,{children:(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`th`,{children:`N\\u00b0 S\\u00e9rie`}),(0,P.jsx)(`th`,{children:`Mod\\u00e8le`}),(0,P.jsx)(`th`,{children:`Affectation`}),(0,P.jsx)(`th`,{children:`Derni\\u00e8re Cl\\u00e9`}),(0,P.jsx)(`th`,{children:`Date Limite`}),(0,P.jsx)(`th`,{children:`Statut Cl\\u00e9`}),(0,P.jsx)(`th`,{style:{textAlign:`center`},children:`Actions`})]})})"

# 4. Active tbody
rep_active_tbody = "[...u.filter(e=>e.date_maj_cle&&e.date_maj_cle.trim()!==``)].sort((e,t)=>{let n=Ye(e),r=Ye(t);return n===r?new Date(e.date_cle_a_faire||`9999-12-31`)-new Date(t.date_cle_a_faire||`9999-12-31`):n-r}).map(e=>(0,P.jsxs)(`tr`,{style:{backgroundColor:I(e)},children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.modele||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{children:e.date_maj_cle||`Non programm\\u00e9e`}),(0,P.jsx)(`td`,{children:e.date_cle_a_faire||`Non d\\u00e9finie`}),(0,P.jsx)(`td`,{children:Xe(e.date_cle_a_faire)}),(0,P.jsxs)(`td`,{style:F.actionsCell,children:[(0,P.jsx)(`button`,{title:`Mettre \\u00e0 jour la cl\\u00e9`,onClick:()=>He(e),style:{...F.actionBtn,color:`#f4a261`,background:`rgba(244, 162, 97, 0.1)`},children:(0,P.jsx)(me,{size:14})}),(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...F.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),(0,P.jsx)(`button`,{title:e.notification_active?`Alerte active (${e.email_notif}) - Cliquer pour modifier`:`Activer une alerte par email`,onClick:()=>Se(e),style:{...F.actionBtn,color:e.notification_active?`#4ade80`:`var(--text-muted)`,background:e.notification_active?`rgba(74, 222, 128, 0.15)`:`rgba(255,255,255,0.05)`},children:e.notification_active?(0,P.jsx)(re,{size:14}):(0,P.jsx)(ne,{size:14})}),(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})])})]},e.id))})"

# 5. Pending thead
rep_pending_thead = "(0,P.jsx)(`thead`,{children:(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`th`,{children:`N\\u00b0 S\\u00e9rie`}),(0,P.jsx)(`th`,{children:`Mod\\u00e8le`}),(0,P.jsx)(`th`,{children:`Affectation`}),(0,P.jsx)(`th`,{style:{textAlign:`center`},children:`Actions`})]})})"

# 6. Pending tbody
rep_pending_tbody = "u.filter(e=>!e.date_maj_cle||e.date_maj_cle.trim()===``).map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.modele||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsxs)(`td`,{style:F.actionsCell,children:[(0,P.jsxs)(`button`,{className:`btn btn-outline`,onClick:()=>He(e),style:{padding:`6px 12px`,fontSize:`0.75rem`,height:`28px`,gap:`4px`},children:[(0,P.jsx)(me,{size:12}),` Initialiser Cl\\u00e9`]}),(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...F.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})])})]},e.id))})"

# Apply all replacements
new_content = content
new_content = new_content.replace(exact_bip_thead, rep_bip_thead)
new_content = new_content.replace(exact_bip_tbody, rep_bip_tbody)
new_content = new_content.replace(exact_active_thead, rep_active_thead)
new_content = new_content.replace(exact_active_tbody, rep_active_tbody)
new_content = new_content.replace(exact_pending_thead, rep_pending_thead)
new_content = new_content.replace(exact_pending_tbody, rep_pending_tbody)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(new_content)

res = subprocess.run(["node", "--check", js_path], capture_output=True, text=True)
if res.returncode == 0:
    print("SUCCESS: All replacements applied and syntax is 100% correct!")
else:
    print("FAILED:")
    print(res.stderr[:500])
