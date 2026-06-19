def check_balance(label, text):
    # Wrap it
    full_text = "(0,P.jsx)('tbody', { children: " + text + " })"
    
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    errors = []
    for i, char in enumerate(full_text):
        if char in '({[':
            stack.append((char, i))
        elif char in ')}]':
            if not stack:
                errors.append(f"Extra closing '{char}' at {i}")
            else:
                top_char, top_idx = stack.pop()
                if pairs[char] != top_char:
                    errors.append(f"Mismatch: '{char}' at {i} doesn't match '{top_char}' at {top_idx}")
                    errors.append(f"  Current char Context: ... {full_text[i-15:i+15]} ...")
                    errors.append(f"  Open char Context: ... {full_text[top_idx-15:top_idx+15]} ...")
    if stack:
        errors.append(f"Unclosed: {[(char, idx) for char, idx in stack]}")
    
    if errors:
        print(f"=== {label} ERRORS ===")
        for err in errors[:10]:
            print(f"  {err}")
    else:
        print(f"=== {label} is PERFECTLY BALANCED ===")

# Base strings stripped of all trailing brackets (ending right after the button's closing parenthesis)
replacement1_base = """u.map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{children:e.statut_activite===`inactif`?(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(230, 57, 70, 0.15)`,color:`#e63946`},children:`Inactif`}):(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(74, 222, 128, 0.15)`,color:`#4ade80`},children:`Actif`})}),(0,P.jsx)(`td`,{style:F.actionsCell,children:(0,P.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:`repeat(2, 1fr)`,gap:`4px`,width:`fit-content`,margin:`auto`},children:[(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}),(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...F.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}),(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})])})"""

replacement2_base = """[...u.filter(e=>e.date_maj_cle&&e.date_maj_cle.trim()!==``)].sort((e,t)=>{let n=Ye(e),r=Ye(t);return n===r?new Date(e.date_cle_a_faire||`9999-12-31`)-new Date(t.date_cle_a_faire||`9999-12-31`):n-r}).map(e=>(0,P.jsxs)(`tr`,{style:{backgroundColor:I(e)},children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{children:e.date_maj_cle||`Non programmée`}),(0,P.jsx)(`td`,{children:e.date_cle_a_faire||`Non définie`}),(0,P.jsx)(`td`,{children:Xe(e.date_cle_a_faire)}),(0,P.jsxs)(`td`,{style:F.actionsCell,children:[(0,P.jsx)(`button`,{title:`Mettre à jour la clé`,onClick:()=>He(e),style:{...F.actionBtn,color:`#f4a261`,background:`rgba(244, 162, 97, 0.1)`},children:(0,P.jsx)(me,{size:14})}),(0,P.jsx)(`button`,{title:e.notification_active?`Alerte active (${e.email_notif}) - Cliquer pour modifier`:`Activer une alerte par email`,onClick:()=>Se(e),style:{...F.actionBtn,color:e.notification_active?`#4ade80`:`var(--text-muted)`,background:e.notification_active?`rgba(74, 222, 128, 0.15)`:`rgba(255,255,255,0.05)`},children:e.notification_active?(0,P.jsx)(re,{size:14}):(0,P.jsx)(ne,{size:14})}),(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})])"""

replacement3_base = """u.filter(e=>!e.date_maj_cle||e.date_maj_cle.trim()===``).map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{style:F.actionsCell,children:(0,P.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:`repeat(2, 1fr)`,gap:`4px`,width:`fit-content`,margin:`auto`},children:[/* Top-left: Cryptage */(0,P.jsx)(`button`,{title:`Mettre à jour la clé`,onClick:()=>He(e),style:{...F.actionBtn,color:`#f4a261`,background:`rgba(244, 162, 97, 0.1)`},children:(0,P.jsx)(me,{size:14})}),/* Top-right: Voir plus */(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...F.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),/* Bottom-left: Empty */(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}),/* Bottom-right: Supprimer */(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})])})"""

replacement4_base = """o.map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`600`},children:e.cis||`N/A`}),(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{children:e.type===`BIP`?(0,P.jsx)(`span`,{style:{color:`var(--text-muted)`},children:`N/A`}):e.date_maj_cle||`Non programmée`}),(0,P.jsx)(`td`,{children:e.type===`BIP`?e.statut_activite===`inactif`?(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(230, 57, 70, 0.15)`,color:`#e63946`},children:`Inactif`}):(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(74, 222, 128, 0.15)`,color:`#4ade80`},children:`Actif`}):e.date_cle_a_faire||`Non définie`}),(0,P.jsx)(`td`,{style:I.actionsCell,children:(0,P.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:`repeat(2, 1fr)`,gap:`4px`,width:`fit-content`,margin:`auto`},children:[/* Top-left: Cryptage */e.type===`BIP`?(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}):(0,P.jsx)(`button`,{title:`Mettre à jour la clé`,onClick:()=>w(e),style:{...I.actionBtn,color:`#f4a261`,background:`rgba(244, 162, 97, 0.1)`},children:(0,P.jsx)(me,{size:13})}),/* Top-right: Voir plus */(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...I.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),/* Bottom-left: Empty */(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}),/* Bottom-right: Supprimer */(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>S(e.id),style:{...I.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:13})})])})"""

# Explicit bracket-concatenated suffixes (without e.id / with e.id)
suffix_with_div = "]" + "}" + ")" + "}" + ")" + "]" + "}" + ",e.id))"
suffix_no_div = "]" + "}" + ")" + "]" + "}" + ",e.id))"

check_balance("Rep 1", replacement1_base + suffix_with_div)
check_balance("Rep 2", replacement2_base + suffix_no_div)
check_balance("Rep 3", replacement3_base + suffix_with_div)
check_balance("Rep 4", replacement4_base + suffix_with_div)
