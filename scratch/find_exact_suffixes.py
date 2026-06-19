replacement1_base = """u.map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{children:e.statut_activite===`inactif`?(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(230, 57, 70, 0.15)`,color:`#e63946`},children:`Inactif`}):(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(74, 222, 128, 0.15)`,color:`#4ade80`},children:`Actif`})}),(0,P.jsx)(`td`,{style:F.actionsCell,children:(0,P.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:`repeat(2, 1fr)`,gap:`4px`,width:`fit-content`,margin:`auto`},children:[(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}),(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...F.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}),(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})])})"""

replacement2_base = """[...u.filter(e=>e.date_maj_cle&&e.date_maj_cle.trim()!==``)].sort((e,t)=>{let n=Ye(e),r=Ye(t);return n===r?new Date(e.date_cle_a_faire||`9999-12-31`)-new Date(t.date_cle_a_faire||`9999-12-31`):n-r}).map(e=>(0,P.jsxs)(`tr`,{style:{backgroundColor:I(e)},children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{children:e.date_maj_cle||`Non programmée`}),(0,P.jsx)(`td`,{children:e.date_cle_a_faire||`Non définie`}),(0,P.jsx)(`td`,{children:Xe(e.date_cle_a_faire)}),(0,P.jsxs)(`td`,{style:F.actionsCell,children:[(0,P.jsx)(`button`,{title:`Mettre à jour la clé`,onClick:()=>He(e),style:{...F.actionBtn,color:`#f4a261`,background:`rgba(244, 162, 97, 0.1)`},children:(0,P.jsx)(me,{size:14})}),(0,P.jsx)(`button`,{title:e.notification_active?`Alerte active (${e.email_notif}) - Cliquer pour modifier`:`Activer une alerte par email`,onClick:()=>Se(e),style:{...F.actionBtn,color:e.notification_active?`#4ade80`:`var(--text-muted)`,background:e.notification_active?`rgba(74, 222, 128, 0.15)`:`rgba(255,255,255,0.05)`},children:e.notification_active?(0,P.jsx)(re,{size:14}):(0,P.jsx)(ne,{size:14})}),(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})])}"""

replacement3_base = """u.filter(e=>!e.date_maj_cle||e.date_maj_cle.trim()===``).map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{style:F.actionsCell,children:(0,P.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:`repeat(2, 1fr)`,gap:`4px`,width:`fit-content`,margin:`auto`},children:[/* Top-left: Cryptage */(0,P.jsx)(`button`,{title:`Mettre à jour la clé`,onClick:()=>He(e),style:{...F.actionBtn,color:`#f4a261`,background:`rgba(244, 162, 97, 0.1)`},children:(0,P.jsx)(me,{size:14})}),/* Top-right: Voir plus */(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...F.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),/* Bottom-left: Empty */(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}),/* Bottom-right: Supprimer */(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>Ve(e.id),style:{...F.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:14})})])})"""

replacement4_base = """o.map(e=>(0,P.jsxs)(`tr`,{children:[(0,P.jsx)(`td`,{style:{fontWeight:`600`},children:e.cis||`N/A`}),(0,P.jsx)(`td`,{style:{fontWeight:`700`},children:e.num_serie||`N/A`}),(0,P.jsx)(`td`,{children:e.affectation||`N/A`}),(0,P.jsx)(`td`,{children:e.type===`BIP`?(0,P.jsx)(`span`,{style:{color:`var(--text-muted)`},children:`N/A`}):e.date_maj_cle||`Non programmée`}),(0,P.jsx)(`td`,{children:e.type===`BIP`?e.statut_activite===`inactif`?(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(230, 57, 70, 0.15)`,color:`#e63946`},children:`Inactif`}):(0,P.jsx)(`span`,{style:{display:`inline-flex`,padding:`2px 8px`,borderRadius:`12px`,fontSize:`0.75rem`,fontWeight:`bold`,background:`rgba(74, 222, 128, 0.15)`,color:`#4ade80`},children:`Actif`}):e.date_cle_a_faire||`Non définie`}),(0,P.jsx)(`td`,{style:I.actionsCell,children:(0,P.jsxs)(`div`,{style:{display:`grid`,gridTemplateColumns:`repeat(2, 1fr)`,gap:`4px`,width:`fit-content`,margin:`auto`},children:[/* Top-left: Cryptage */e.type===`BIP`?(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}):(0,P.jsx)(`button`,{title:`Mettre à jour la clé`,onClick:()=>w(e),style:{...I.actionBtn,color:`#f4a261`,background:`rgba(244, 162, 97, 0.1)`},children:(0,P.jsx)(me,{size:13})}),/* Top-right: Voir plus */(0,P.jsx)(`button`,{title:`Voir plus d'informations`,onClick:()=>window.showEquipmentDetails(e),style:{...I.actionBtn,color:`#3b82f6`,background:`rgba(59, 130, 246, 0.1)`},children:(0,P.jsxs)(`svg`,{width:14,height:14,viewBox:`0 0 24 24`,fill:`none`,stroke:`currentColor`,strokeWidth:2.5,strokeLinecap:`round`,strokeLinejoin:`round`,children:[(0,P.jsx)(`path`,{d:`M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z`}),(0,P.jsx)(`circle`,{cx:12,cy:12,r:3})]})}),/* Bottom-left: Empty */(0,P.jsx)(`div`,{style:{width:`28px`,height:`28px`}}),/* Bottom-right: Supprimer */(0,P.jsx)(`button`,{title:`Supprimer l'appareil`,onClick:()=>S(e.id),style:{...I.actionBtn,color:`#e63946`,background:`rgba(230, 57, 70, 0.1)`},children:(0,P.jsx)(Ne,{size:13})})])})"""

def find_suffix_to_balance(label, base_text):
    # Wrap base text as if it was in the JSX tree
    # (0,P.jsx)('tbody', { children: base_text + suffix })
    full_text = "(0,P.jsx)('tbody', { children: " + base_text
    
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    match_pairs = {'(': ')', '{': '}', '[': ']'}
    
    for i, char in enumerate(full_text):
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack:
                print(f"[{label}] Unexpected closing char '{char}' at {i}")
            else:
                top = stack.pop()
                if pairs[char] != top:
                    print(f"[{label}] Mismatch at {i}: '{char}' doesn't match '{top}'")
                    # Put it back to trace
                    stack.append(top)
                    
    # The stack now contains unclosed opening brackets in order.
    # To close them, we must output their matching closing brackets in reverse order.
    suffix = ""
    for char in reversed(stack):
        suffix += match_pairs[char]
        
    # Wait, the wrapping was: "(0,P.jsx)('tbody', { children: " (which adds `(`, `{`, `[` to the stack)
    # The final balance check of the full expression must include:
    # - closing the children value (if we were inside the map callback, it needs `)` etc)
    # - closing the children array of tbody `]`
    # - closing the tbody props object `}`
    # - closing the tbody call `)`
    # Since our stack has these, the suffix we computed actually includes the closing of the tbody wrapper.
    # Let's strip the closing of the tbody wrapper to get the suffix for the base_text alone!
    # The tbody wrapper has:
    # 1. `(` of `(0,P.jsx)`
    # 2. `{` of props
    # 3. `[` of map? No, tbody children is the map call, so children: base_text.
    # If base_text starts with `u.map` or `o.map`, it has:
    # 4. `(` of `map(`
    # 5. `(` of `e=>`? No, callback is `e=>tr`.
    # Let's see what is inside the stack.
    print(f"=== {label} STACK ===")
    print("Stack of unclosed open chars:", stack)
    # Let's check if we can verify the suffix directly by appending it and testing balance
    candidate = base_text + suffix
    
    # Wait, let's trace: does `candidate` balance the tbody wrapper itself?
    # Yes, because `suffix` is calculated from `(0,P.jsx)('tbody', { children: base_text`!
    # So `(0,P.jsx)('tbody', { children: base_text + suffix })` is perfectly balanced!
    # But wait, in the bundle, is the base_text wrapped in `(0,P.jsx)('tbody', { children: ... })`?
    # Let's check.
    # For Rep 1, the target in the bundle is:
    # `(0,P.jsx)(`tbody`,{children: u.map(...)})`
    # Yes! It is the children value of the `tbody` tag.
    # So yes, it is EXACTLY wrapped in `(0,P.jsx)(`tbody`,{children: ...})`!
    # So `suffix` should close the `map` callback, key, `tr` call, and then... wait!
    # Does `suffix` include `})` for tbody?
    # Yes! The last three items on the stack will be `(`, `{` from `(0,P.jsx)('tbody', { children:`
    # So the suffix will end with `})`!
    # Since we want to replace only the children of tbody, the replaced content in the bundle should NOT close the tbody itself! The tbody closing tag in the bundle is outside our search-and-replace block!
    # Let's verify this.
    # In apply_replacements.py:
    # idx_bip_tbody = content.find("u.map(e=>(0,P.jsxs)(`tr`", idx_bip_thead_end)
    # idx_bip_tbody_end = content.find(",e.id))})", idx_bip_tbody) + 9
    # exact_bip_tbody = content[idx_bip_tbody:idx_bip_tbody_end]
    # Wait! The search string ends with `,e.id))})`.
    # Let's look at the length of `exact_bip_tbody`:
    # The trailing `})` at the end of `,e.id))})` actually closes the `tbody`!
    # Ah!
    # `(0,P.jsx)(`tbody`,{children: u.map(...)})`
    # In the bundle, it is:
    # `(0,P.jsx)(`tbody`,{children: u.map(...)})`
    # So `exact_bip_tbody` starts with `u.map` and ends with `,e.id))})` which closes:
    # - `tr` call: `)`
    # - `map` call: `)`
    # - `tbody` call: `})`
    # So the replacement block MUST end with the closing of tbody too!
    # Yes! So the `suffix` computed from `(0,P.jsx)('tbody', { children: base_text` is EXACTLY the replacement block we want!
    # Let's test if the candidate with suffix works:
    check_text = "(0,P.jsx)('tbody', { children: " + base_text + suffix
    print("Computed suffix:", repr(suffix))
    # Let's check balance of check_text
    st = []
    for c in check_text:
        if c in '({[': st.append(c)
        elif c in ')}]': st.pop()
    print("Remaining stack for check_text (should be empty):", st)
    print()

find_suffix_to_balance("Rep 1", replacement1_base)
find_suffix_to_balance("Rep 2", replacement2_base)
find_suffix_to_balance("Rep 3", replacement3_base)
find_suffix_to_balance("Rep 4", replacement4_base)
