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

replacement3_base = """u.filter(e=>!e.date_maj_cle||e.date_maj_cle.trim()===``).map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{style:F.actionsCell,children:(0,P.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:`repeat(2, 1fr)`,gap:`4px`,width:`fit-content`,margin:`auto`},children:[/* Top-left: Cryptage */(0,P.jsx)(`button`,{title:`Mettre à jour la clé`,onClick:()=>He(e),style:{...F.actionBtn,color:`#f4a261`,background:`rgba(244, 162, 97, 0.1)`},children:(0,P.jsx)(me,{size:14})}),/* Top-right: Voir plus */(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...F.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),/* Bottom-left: Empty */(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}),/* Bottom-right: Supprimer */(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})"""

candidate = replacement3_base + "]})})]},e.id))"
check_balance("Replacement 3 Candidate", candidate)
