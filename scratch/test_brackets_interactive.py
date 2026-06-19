text = """u.map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{children:e.statut_activite===`inactif`?(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(230, 57, 70, 0.15)`,color:`#e63946`},children:`Inactif`}):(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(74, 222, 128, 0.15)`,color:`#4ade80`},children:`Actif`})}),(0,P.jsx)(`td`,{style:F.actionsCell,children:(0,P.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:`repeat(2, 1fr)`,gap:`4px`,width:`fit-content`,margin:`auto`},children:[(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}),(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...F.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}),(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})])})"""

full_text = "(0,P.jsx)('tbody', { children: " + text

stack = []
pairs = {')': '(', '}': '{', ']': '['}

for i, char in enumerate(full_text):
    if char in '({[':
        stack.append((char, i))
    elif char in ')}]':
        if not stack:
            print(f"Extra closing '{char}' at index {i}: ... {full_text[i-15:i+15]} ...")
        else:
            top_char, top_idx = stack.pop()
            if pairs[char] != top_char:
                print(f"Mismatch: '{char}' at index {i} doesn't match '{top_char}' at index {top_idx}")
                print(f"  Current char context: ... {full_text[i-15:i+15]} ...")
                print(f"  Open char context: ... {full_text[top_idx-15:top_idx+15]} ...")
                # Put it back to prevent cascade of errors
                stack.append((top_char, top_idx))

print("Final Stack:", stack)
